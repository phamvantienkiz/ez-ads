# 10. Folder Structure Invariants — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 1.0  
**Last Updated**: 2026-10-17  

---

## 1. Master Repository Layout

Cấu trúc thư mục của dự án BAHA Ads Manager được chuẩn hóa phân chia độc lập giữa Backend và Frontend, nghiêm cấm đặt các tệp lộn xộn ngoài thư mục quy định:

```
E:\MyProject\BAHA\
├── backend/                           # FastAPI Application Root
│   ├── app/
│   │   ├── core/                      # Core configuration & database init
│   │   │   ├── config.py              # Environment settings (Pydantic BaseSettings)
│   │   │   └── database.py            # SQLite connection & schema initialization
│   │   ├── models/                    # Internal data models (if needed)
│   │   ├── schemas/                   # Pydantic V2 Request & Response schemas
│   │   │   ├── auth_schemas.py
│   │   │   └── ad_schemas.py
│   │   ├── repositories/              # SQLite Data Access Layer
│   │   │   ├── session_repository.py  # meta_sessions queries
│   │   │   └── run_repository.py      # ad_creation_runs queries
│   │   ├── services/                  # Business Logic & API Clients
│   │   │   ├── meta_client.py         # httpx calls to Meta Graph API v20.0
│   │   │   └── ad_service.py          # 5-step creation orchestrator
│   │   ├── routers/                   # FastAPI API Endpoints
│   │   │   ├── health.py              # GET /api/health
│   │   │   ├── meta_auth.py           # GET /api/meta/connect, callback, status
│   │   │   ├── meta_assets.py         # GET /api/meta/ad-accounts, pages
│   │   │   └── ads.py                 # POST /api/ads, GET /api/campaigns
│   │   └── main.py                    # FastAPI application factory & CORS setup
│   ├── tests/                         # Backend Unit & Integration Tests
│   ├── pyproject.toml                 # Dependency definition (or requirements.txt)
│   ├── requirements.txt               # Locked dependencies
│   └── .env.example                   # Environment configuration template
│
├── frontend/                          # Next.js Application Root
│   ├── src/
│   │   ├── app/                       # Next.js App Router (Layout & Pages)
│   │   │   ├── layout.tsx             # Root layout with Tailwind CSS
│   │   │   ├── page.tsx               # Main Dashboard & Tab Switcher
│   │   │   └── globals.css            # Tailwind directives
│   │   ├── components/                # Modular React Components
│   │   │   ├── Header.tsx             # Top bar with connection status
│   │   │   ├── ConnectCard.tsx        # OAuth connect / disconnect actions
│   │   │   ├── AssetSelector.tsx      # Ad Account & Page selection dropdowns
│   │   │   ├── AdForm.tsx             # Product Ad creation form
│   │   │   ├── AdPreviewCard.tsx      # Facebook Link Ad simulated card
│   │   │   ├── ResultPanel.tsx        # Success / Partial Failure real IDs display
│   │   │   └── CampaignTable.tsx      # Real campaigns list with Refresh button
│   │   ├── services/                  # Frontend API Client
│   │   │   └── api.ts                 # Fetch wrapper calling FastAPI (:8000)
│   │   └── types/                     # Shared TypeScript interfaces
│   │       └── index.ts               # Account, Page, Campaign, Run types
│   ├── package.json                   # Frontend dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   └── tailwind.config.js             # Tailwind CSS configuration
│
├── docs/                              # 3-Layer Documentation System
│   ├── business/                      # Business goals, BRD, Roadmap, Glossary
│   ├── architecture/                  # Single Source of Truth for Architecture
│   ├── implementation/                # Release-specific PRDs, Stories, ACs
│   └── views/                         # Standalone interactive HTML views
│
├── tasks/                             # Agent Task Tracking & Lessons
│   ├── todo.md
│   └── lessons.md
│
├── AGENTS.md                          # Project Intelligence & Agent Control Layer
└── README.md                          # Quickstart & Demo Guidelines
```

---

## 2. Structural Invariants (Ràng buộc bất biến)

1. **Virtual Environment Isolation**: Toàn bộ thư viện Python bắt buộc nằm trong `backend/.venv/`. Tuyệt đối không cài đặt vào global system.
2. **Node Modules Isolation**: Toàn bộ thư viện Node.js bắt buộc nằm trong `frontend/node_modules/`.
3. **Database File Location**: Tệp SQLite `baha_ads_manager.db` phải nằm trong thư mục gốc `backend/` hoặc thư mục gốc dự án theo cấu hình `DATABASE_URL`.
