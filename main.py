import os
import time
import asyncio
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
from pypdf import PdfReader
from docx import Document
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import win32security  # Windows 專用權限套件

# 引入 dotenv 以讀取環境變數 (模擬真實開發環境)
from dotenv import load_dotenv

# 載入 .env 設定
load_dotenv()

app = FastAPI(title="Enterprise AI Workflow Automation")

# ==========================================
# 🔔 設定區 (從環境變數讀取，確保資安)
# ==========================================
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
AI_MODEL = os.getenv("AI_MODEL", "qwen2.5:3b")

# 允許跨域請求 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 📂 檔案路徑設定
# ==========================================
# 注意：在實際部署時，請修改為實際的 NAS 或內網掛載路徑
SEARCH_DIRS = [
    # Path(r"\\192.168.1.10\Public\Project_Docs"),  # 範例：公司內網路徑
    Path("./demo_data/documents"),                 # 範例：本地測試路徑
    Path("C:/Users/User/Documents/Projects"),      # 範例：本地文件
]

# 智慧關鍵字定義 (用於自動分類專案)
PROJECT_DEFINITIONS = {
    "Project-Alpha": ["Alpha", "Gen1"],
    "Project-Beta":  ["Beta"],
    "Project-Gamma": ["Gamma", "Monitoring"],
}

# 忽略清單 (黑名單)
IGNORED_DIRS = {".git", ".vscode", "__pycache__", "node_modules", "Backup", "Temp"}
IGNORED_EXTENSIONS = {".dll", ".exe", ".tmp", ".log", ".bak"}

# 需要掃描擁有者的檔案類型
OWNER_LOOKUP_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}


# ==========================================
# 🛠️ 核心功能函式
# ==========================================

def send_teams_card(title, summary, facts):
    """
    發送 Adaptive Card 到 Microsoft Teams
    """
    if not TEAMS_WEBHOOK_URL or "http" not in TEAMS_WEBHOOK_URL:
        print("⚠️ 未設定 Teams Webhook，跳過通知")
        return

    adaptive_facts = [{"title": f['name'], "value": f['value']} for f in facts]
    
    card_payload = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium", "color": "Accent"},
                    {"type": "TextBlock", "text": f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "isSubtle": True, "size": "Small"},
                    {"type": "FactSet", "facts": adaptive_facts},
                    {"type": "TextBlock", "text": "📊 AI Analysis Summary:", "weight": "Bolder", "size": "Small", "separator": True},
                    {"type": "TextBlock", "text": summary, "wrap": True, "size": "Small"}
                ]
            }
        }]
    }

    try:
        requests.post(TEAMS_WEBHOOK_URL, json=card_payload, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"❌ Teams 發送失敗: {e}")


def read_file_content(file_path):
    """
    多格式檔案讀取器 (支援 PDF, Docx, Excel, Code)
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    content = ""
    
    try:
        if ext in ['.c', '.h', '.cpp', '.py', '.js', '.txt', '.md', '.json']:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
        elif ext == '.pdf':
            reader = PdfReader(path)
            for page in reader.pages[:30]: # 限制頁數
                text = page.extract_text()
                if text: content += text + "\n"
            if not content.strip(): return "[系統警告：無法讀取 PDF 文字，可能是掃描檔]"

        elif ext == '.docx':
            doc = Document(path)
            content = "\n".join([para.text for para in doc.paragraphs])
            
        elif ext in ['.xlsx', '.xls']:
            xls = pd.ExcelFile(path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, nrows=400) # 限制行數
                content += f"\n=== Sheet: {sheet_name} ===\n" + df.to_csv(index=False)

        else:
            return f"[不支援的格式：{ext}]"

        return content[:5000] # 限制字數以防 Token 超出
        
    except Exception as e:
        return f"[讀取錯誤：{str(e)}]"


def get_file_owner(path_str):
    """取得 Windows 檔案擁有者 (需 Windows 環境)"""
    try:
        sd = win32security.GetFileSecurity(path_str, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return name
    except:
        return "Unknown"


def determine_project(file_path_obj):
    """根據檔名與路徑關鍵字判斷所屬專案"""
    full_path = str(file_path_obj).lower()
    filename = file_path_obj.name.lower()
    scores = {}
    
    for project, keywords in PROJECT_DEFINITIONS.items():
        score = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in filename: score += 10
            elif kw_lower in full_path: score += 3
        if score > 0: scores[project] = score
            
    return max(scores, key=scores.get) if scores else "Uncategorized"


def internal_scan_files():
    """掃描指定目錄下的所有檔案"""
    all_results = []
    for base_dir in SEARCH_DIRS:
        if not base_dir.exists(): continue
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS] # 過濾資料夾
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in IGNORED_EXTENSIONS: continue
                
                try:
                    stat = file_path.stat()
                    if stat.st_size == 0: continue
                    
                    all_results.append({
                        "filename": file_path.name,
                        "path": str(file_path),
                        "project": determine_project(file_path),
                        "updated_at": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                        "owner": get_file_owner(str(file_path)) if file_path.suffix.lower() in OWNER_LOOKUP_EXTENSIONS else "",
                        "raw_mtime": stat.st_mtime
                    })
                except: pass
    
    all_results.sort(key=lambda x: x['raw_mtime'], reverse=True)
    return all_results

# ==========================================
# 🚀 API 路由區
# ==========================================

class AnalyzeRequest(BaseModel):
    files: list

@app.post("/api/analyze_local")
def analyze_local_files(request: AnalyzeRequest):
    """接收檔案清單，呼叫 Local LLM 進行分析"""
    context = "你是一位專業的專案經理。請總結以下檔案重點：\n\n"
    for file_path in request.files:
        content = read_file_content(file_path)
        context += f"=== File: {Path(file_path).name} ===\n{content}\n\n"
    
    try:
        res = requests.post(OLLAMA_API_URL, json={
            "model": AI_MODEL, "prompt": context, "stream": False
        })
        return {"status": "success", "content": res.json().get('response', '')}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/scan")
def scan_projects():
    """觸發檔案掃描"""
    return {"files": internal_scan_files()}

async def run_weekly_report_job():
    """背景任務：生成周報"""
    # 這裡模擬掃描最近 7 天的異動
    files = internal_scan_files()
    recent_files = [f for f in files if (time.time() - f['raw_mtime']) < 7*24*3600]
    
    if not recent_files:
        send_teams_card("Weekly Report", "No updates this week.", [])
        return

    # 簡單分組並發送通知 (邏輯簡化版)
    grouped = defaultdict(list)
    for f in recent_files: grouped[f['project']].append(f['filename'])
    
    summary = f"Detected updates in {len(grouped)} projects. Proceeding with analysis..."
    send_teams_card("Weekly Report Started", summary, [])
    # (後續 AI 分析邏輯同上，為簡潔省略)

@app.get("/api/trigger_report")
async def trigger_report(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(run_weekly_report_job)
    return {"status": "started", "message": "Report generation running in background..."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
