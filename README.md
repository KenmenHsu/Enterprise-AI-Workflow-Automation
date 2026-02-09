# Enterprise AI Workflow Automation 

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![RAG](https://img.shields.io/badge/AI-RAG%20System-orange)]()
[![Local LLM](https://img.shields.io/badge/Model-Local%20LLM-purple)]()

## 專案簡介 (Introduction)

這是一個專為企業環境設計的 **自動化工作流系統 (Enterprise AI Workflow System)**，旨在解決內部資訊分散與報告撰寫耗時的問題。

本系統結合了 **Local LLM (本地大型語言模型)** 與 **RAG (檢索增強生成)** 技術，能夠在 **確保資料隱私（不需上傳至外部 API）** 的前提下，自動讀取內部網路的專案文件，並生成結構化的周報與進度摘要。系統同時提供現代化的 Web 儀表板，讓團隊能直觀地管理與分析資料。

An automated workflow system designed for enterprise environments to solve information fragmentation. Leveraging **Local LLM** and **RAG**, it automatically ingests internal documents and generates structured weekly reports while ensuring data privacy (no external API calls required).

---

## 核心功能 (Key Features)

* **隱私優先 (Privacy First)**：全本地端運行 (Local LLM)，確保敏感的專案數據不會流出企業內網。
* **智能文檔檢索 (Smart Retrieval)**：自動掃描並索引資料夾中的 PDF, Docx, Excel, Txt 文件，並依照專案名稱自動分類。
* **互動式儀表板 (Interactive Dashboard)**：
    * 提供現代化 Web 介面 (Vue.js + Tailwind CSS)。
    * 支援關鍵字搜尋、分類過濾、一鍵複製檔案路徑。
* **AI 深度解讀 (AI Analysis)**：
    * 勾選檔案後，由 AI 自動進行跨文檔摘要與重點分析。
    * 自動識別專案風險與進度瓶頸。
* **自動化匯報 (Auto-Reporting)**：整合 Microsoft Teams Webhook，定時自動推播專案週報。

---

## 技術架構 (Tech Stack)

* **Backend (後端)**: Python 3.10+, FastAPI, Uvicorn
* **Frontend (前端)**: HTML5, Vue.js 3, Tailwind CSS
* **AI Engine (模型)**: Ollama (Running Qwen/Llama3 locally)
* **Integration**: Microsoft Teams Webhook
* **Tools**: Pandas (Excel/CSV processing), PyPDF, python-docx

---

## 專案結構 (Structure)

```text
Enterprise-AI-Workflow-Automation/
├── 📄 .env.example        # 環境變數範本 (資安設定)
├── 📄 .gitignore          # Git 忽略清單
├── 📄 main.py             # 後端核心程式 (FastAPI Server)
├── 📄 requirements.txt    # 專案依賴套件清單
└── 📂 webui/              # 前端介面資料夾
    └── 📄 index.html      # 儀表板入口 (Dashboard)
```

---

## 快速開始 (Quick Start)

### 1. 下載專案 & 安裝依賴
```bash
# 1. Clone 本專案
git clone https://github.com/KenmenHsu/Enterprise-AI-Workflow-Automation.git

# 2. 進入資料夾
cd Enterprise-AI-Workflow-Automation

# 3. 安裝 Python 套件
pip install -r requirements.txt
```

### 2. 設定環境變數
為了保護隱私，請將 `.env.example` 複製一份並改名為 `.env`，然後填入您的設定：
```ini
# .env 檔案內容範例
TEAMS_WEBHOOK_URL=https://your-teams-webhook-url-here
OLLAMA_API_URL=http://localhost:11434/api/generate
AI_MODEL=qwen2.5:3b
```

### 3. 啟動服務
**步驟一：啟動後端 API**
```bash
python main.py
```
*看到 `Application startup complete` 代表啟動成功，後端預設在 `http://localhost:8001`。*

**步驟二：開啟前端介面**
直接用瀏覽器打開 `webui/index.html` 檔案即可開始使用！

---

## 系統截圖 (Screenshots)

### 1. 研發資料管理儀表板 (R&D Dashboard)
> <img width="1339" height="641" alt="html" src="https://github.com/user-attachments/assets/2c79f5e8-640c-4c86-be57-96279e7190bd" />

> <img width="1339" height="641" alt="send AI" src="https://github.com/user-attachments/assets/f0afed0d-9d1d-4fbc-95aa-e1908c760bba" />

### 2. AI 深度解讀報告範例
> <img width="628" height="536" alt="AI report" src="https://github.com/user-attachments/assets/7fc23131-71f3-4dc0-a103-0e569bb77e6c" />
> <img width="354" height="284" alt="teams report" src="https://github.com/user-attachments/assets/ad072c73-6de7-4a47-864c-87574835f48b" />

---

## 👤 作者 (Author)

**Kenmen Hsu**
* Focus on: AI Application Planning, Medical Electronics, System Integration
* [GitHub Profile](https://github.com/KenmenHsu)






