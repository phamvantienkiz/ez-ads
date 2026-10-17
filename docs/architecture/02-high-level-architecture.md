# 02. High-Level Architecture — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 1.0  
**Last Updated**: 2026-10-17  

---

## 1. Architectural Style & Overview

Hệ thống **BAHA Ads Manager MVP** được thiết kế theo mô hình **Client-Server 2 tầng tối giản (Decoupled Single-Page Web App + Headless API Server)**, tối ưu hóa cho mục tiêu hoàn thành luồng demo end-to-end trong vòng 2 giờ.

### Các nguyên tắc kiến trúc cốt lõi:
1. **Server-Side API Proxy & Token Isolation**: Mọi giao tiếp với Meta Graph API và việc lưu trữ bí mật (App Secret, Access Token) được cô lập hoàn toàn tại Backend FastAPI. Frontend Next.js không trực tiếp gọi Meta API hay giữ token.
2. **Minimal State Persistence**: Sử dụng SQLite cục bộ với 2 bảng chuyên biệt (`meta_sessions` và `ad_creation_runs`) để duy trì phiên làm việc và lịch sử thực thi mà không cần hạ tầng database phức tạp.
3. **Synchronous Deterministic Orchestration**: Chuỗi tạo 5 tài nguyên trên Meta Marketing API được thực thi tuần tự, đồng bộ phía backend, ghi nhận chính xác trạng thái từng bước và phản hồi trung thực về UI (kể cả khi thất bại một phần).

---

## 2. High-Level System Topology

```mermaid
flowchart TB
    subgraph ClientTier ["1. Client Tier (Browser)"]
        UI["Next.js Single Page App<br/>(React + TypeScript + Tailwind CSS)<br/>Port: 3000"]
    end

    subgraph ServerTier ["2. Application Server Tier (Local Host)"]
        FastAPI["FastAPI Web Framework<br/>(Uvicorn ASGI Server)<br/>Port: 8000"]
        
        subgraph Submodules ["Internal Modules"]
            Router["API Routers<br/>(/api/meta, /api/ads, /api/campaigns)"]
            Service["Meta Orchestration Service<br/>(httpx Async Client)"]
            Repo["SQLite Session & Run Repository<br/>(aiosqlite / sqlite3)"]
        end
        
        Router --> Service
        Router --> Repo
        Service --> Repo
    end

    subgraph DataTier ["3. Data Tier (Local File)"]
        DB[(baha_ads_manager.db<br/>SQLite File)]
    end

    subgraph ExternalTier ["4. External Meta Platform"]
        MetaAuth["Meta OAuth 2.0 Gateway<br/>https://www.facebook.com/v20.0/dialog/oauth"]
        MetaGraph["Meta Graph & Marketing API v20.0<br/>https://graph.facebook.com/v20.0/"]
    end

    UI <-->|HTTP / REST JSON<br/>(Proxied / CORS)| FastAPI
    Repo <-->|Embedded SQL| DB
    FastAPI <-->|1. OAuth Exchange| MetaAuth
    Service <-->|2. Assets & Sequential 5 Creation APIs| MetaGraph
```

---

## 3. Communication & Data Flow Overview

| Tuyến kết nối | Giao thức | Định dạng dữ liệu | Mục đích |
|---|---|---|---|
| **Client $\rightarrow$ FastAPI Server** | HTTP / 1.1 | JSON (UTF-8) | Chuyển hướng OAuth, lấy trạng thái, chọn tài khoản/page, gửi form tạo quảng cáo. |
| **FastAPI $\rightarrow$ Meta OAuth** | HTTPS | Form URL Encoded / JSON | Trao đổi Authorization Code lấy User Access Token, xác minh `state`. |
| **FastAPI $\rightarrow$ Meta Graph API** | HTTPS | JSON / REST (`Authorization: Bearer`) | Lấy Ad Accounts, Pages, Campaigns và gửi chuỗi 5 requests tạo tài nguyên quảng cáo. |
| **FastAPI $\rightarrow$ SQLite** | C-Library / Driver | SQL B-Tree | Đọc/ghi 1 phiên đăng nhập (`meta_sessions`) và ghi log lịch sử (`ad_creation_runs`). |

---

## 4. Architectural Boundaries & Non-Goals

- **Không dùng Microservices**: Toàn bộ nghiệp vụ backend nằm trong 1 service FastAPI nguyên khối (modular monolith) gọn nhẹ.
- **Không dùng Message Queue / Worker (Redis / Celery)**: Luồng demo phục vụ 1 người dùng trực tiếp, việc điều phối chuỗi API được thực thi trực tiếp trong request handler với timeout hợp lý (~30s).
- **Không dùng Storage Cloud (S3 / GCS)**: Hình ảnh sản phẩm được truyền thông qua Image URL công khai có sẵn; backend chỉ gọi endpoint băm ảnh của Meta mà không lưu trữ file nhị phân.
