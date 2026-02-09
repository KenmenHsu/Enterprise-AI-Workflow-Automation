# Enterprise AI Workflow Automation

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![RAG](https://img.shields.io/badge/AI-RAG%20System-orange)]()
[![Local LLM](https://img.shields.io/badge/Model-Local%20LLM-purple)]()

-專案簡介 (Introduction)
這是一個專為企業環境設計的[自動化工作流系統]，旨在解決內部資訊分散與報告撰寫耗時的問題。
本系統結合了 "Local LLM" 與 "RAG" 技術，能夠在確保資料隱私（不需上傳至外部 API）的前提下，自動讀取內部網路的專案文件，並生成結構化的周報與進度摘要。

An automated workflow system designed for enterprise environments to solve information fragmentation. Leveraging "Local LLM" and "RAG", it automatically ingests internal documents and generates structured weekly reports while ensuring data privacy (no external API calls required).

---

-核心功能 (Key Features)

 "隱私優先 (Privacy First)"：全本地端運行，確保敏感的專案數據不會流出企業內網。
 "智能文檔檢索 (Smart Retrieval)"：自動掃描並索引內部網路共享資料夾中的 PDF、Docx、Txt 文件。
 "自動化周報 (Auto-Reporting)"：
    自動彙整團隊成員的進度更新。
    識別專案風險與延遲項目。
    生成符合管理層需求的摘要報告。
 "虛擬主管助理"：提供 Chat 介面，允許使用者針對專案歷史紀錄進行問答（例如：「上個月專案的主要瓶頸是什麼？」）。

---

-技術架構 (Tech Stack)

 核心語言: Python 3.10+
 LLM 整合: Ollama / Local Inference Server
 RAG 框架: LangChain / LlamaIndex
 向量資料庫: ChromaDB / FAISS
 後端 API: FastAPI
 自動化排程: Celery / APScheduler

---

-快速開始 (Quick Start)

1. 安裝依賴
```bash
git clone [https://github.com/KenmenHsu/Enterprise-AI-Workflow-Automation.git](https://github.com/KenmenHsu/Enterprise-AI-Workflow-Automation.git)
cd Enterprise-AI-Workflow-Automation
pip install -r requirements.txt