# 03. Service Architecture — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 1.0  
**Last Updated**: 2026-10-17  

---

## 1. Backend Service Layering (FastAPI Layered Pattern)

Kiến trúc backend tuân thủ cấu trúc phân tầng nghiêm ngặt (Router $\rightarrow$ Service $\rightarrow$ Repository) nhằm bảo đảm mã nguồn dễ bảo trì, dễ kiểm thử và không bị trộn lẫn nghiệp vụ gọi Meta API vào tầng tiếp nhận HTTP request.

```
┌────────────────────────────────────────────────────────┐
│                   ROUTER LAYER (HTTP)                  │
│  - meta_auth_router.py   (OAuth & Token status)        │
│  - meta_assets_router.py (Ad Accounts & Pages)         │
│  - ads_router.py         (Create Ad & Campaign list)   │
│  - health_router.py      (Health check)                │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                   SERVICE LAYER (Core)                 │
│  - MetaAuthService   (State verify, Code exchange)     │
│  - MetaClientService (httpx wrapper for Meta v20.0)    │
│  - AdCreationService (Sequential 5 API Orchestrator)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                 REPOSITORY LAYER (Data)                │
│  - SessionRepository (meta_sessions: read/write token) │
│  - RunRepository     (ad_creation_runs: save results)  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Service Responsibilities Breakdown

### 2.1. Router Layer (`backend/app/routers/`)
- Tiếp nhận HTTP request, phân giải tham số và validate dữ liệu đầu vào qua **Pydantic V2 Schemas**.
- Bắt các ngoại lệ nghiệp vụ và trả về HTTP response với chuẩn phong bì (Consistent Envelope):
  `{"success": bool, "data": Any, "message": str, "error": dict}`.
- Không chứa logic nghiệp vụ tính toán ngân sách hay cấu trúc payload Meta.

### 2.2. Service Layer (`backend/app/services/`)
- **`MetaAuthService`**:
  - Sinh URL đăng nhập OAuth với các scopes bắt buộc: `ads_management`, `ads_read`, `pages_read_engagement`, `pages_manage_ads`, `public_profile`.
  - Sinh và đối soát tham số `state` chống tấn công CSRF.
  - Đổi `code` lấy User Access Token ngắn hạn; lưu token vào repository.
- **`MetaClientService`**:
  - Đóng gói HTTP Client (`httpx.AsyncClient`) với timeout 30s.
  - Tự động gắn header `Authorization: Bearer <token>`.
  - Thực thi các lời gọi truy vấn: `/me/adaccounts`, `/me/accounts`, `/{ad_account_id}/campaigns`.
- **`AdCreationService`**:
  - Điều phối chuỗi 5 lời gọi tạo tài nguyên tuần tự (Sequential Pipeline):
    1. Băm ảnh $\rightarrow$ `image_hash`.
    2. Tạo Campaign $\rightarrow$ `campaign_id` (status: `PAUSED`).
    3. Quy đổi tiền tệ và tạo Ad Set $\rightarrow$ `adset_id` (status: `PAUSED`).
    4. Tạo Ad Creative liên kết Fanpage và `image_hash` $\rightarrow$ `creative_id`.
    5. Tạo Ad liên kết Ad Set và Creative $\rightarrow$ `ad_id` (status: `PAUSED`).
  - Ghi nhận trạng thái: `success`, `partial_failure`, hoặc `failed`.
  - Làm sạch thông báo lỗi Meta (loại bỏ token/secrets).

### 2.3. Repository Layer (`backend/app/repositories/`)
- Tương tác trực tiếp với file SQLite `baha_ads_manager.db`.
- **`SessionRepository`**: Đọc/Ghi duy nhất 1 bản ghi phiên đăng nhập (`id=1`). Cung cấp phương thức `get_current_token()` và `save_session()`.
- **`RunRepository`**: Ghi bản ghi phiên chạy vào `ad_creation_runs` và đọc phiên chạy mới nhất `get_latest_run()`.

---

## 3. In-Memory Session & Concurrency Management

- Vì đây là ứng dụng phục vụ demo trực tiếp cho 1 người vận hành, hệ thống áp dụng cơ chế **Idempotency Lock** đơn giản trong bộ nhớ của backend (hoặc cờ `is_creating` ở frontend) nhằm ngăn chặn việc nhấn đúp (double-click) gây tạo trùng chiến dịch trên tài khoản quảng cáo.
