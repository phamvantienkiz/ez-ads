# Database Migration & Schema Setup — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Database**: SQLite 3 (`baha_ads_manager.db`)  
**Ngày cập nhật**: 2026-10-17  

---

## 1. Migration Strategy (Tự động khởi tạo)

Đối với phiên bản MVP Demo 2 giờ, hệ thống áp dụng cơ chế **Zero-Config Auto-Migration**:
- Khi ứng dụng FastAPI khởi chạy (`app/main.py`), hàm lifespan `init_db()` sẽ tự động kiểm tra và thực thi script DDL nếu các bảng chưa tồn tại.
- Không yêu cầu cài đặt hay cấu hình công cụ migration phức tạp (như Alembic) để tiết kiệm tối đa thời gian triển khai.

---

## 2. Migration 001: Initial Schema

### Up Migration Script (Khởi tạo 2 bảng cốt lõi)
```sql
-- 1. Bảng lưu trữ phiên làm việc Meta OAuth duy nhất
CREATE TABLE IF NOT EXISTS meta_sessions (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    access_token TEXT NOT NULL,
    token_type TEXT DEFAULT 'bearer',
    expires_at INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng lưu trữ lịch sử các lần chạy tạo chiến dịch quảng cáo
CREATE TABLE IF NOT EXISTS ad_creation_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_account_id TEXT NOT NULL,
    page_id TEXT NOT NULL,
    campaign_id TEXT,
    adset_id TEXT,
    creative_id TEXT,
    ad_id TEXT,
    status TEXT NOT NULL CHECK (status IN ('pending', 'success', 'partial_failure', 'failed')),
    request_summary TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chỉ mục tối ưu hóa truy vấn phiên chạy mới nhất
CREATE INDEX IF NOT EXISTS idx_runs_created_at ON ad_creation_runs(created_at DESC);
```

### Down Migration Script (Rollback sạch)
```sql
DROP INDEX IF EXISTS idx_runs_created_at;
DROP TABLE IF EXISTS ad_creation_runs;
DROP TABLE IF EXISTS meta_sessions;
```
