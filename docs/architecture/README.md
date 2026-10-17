# Architecture Map & System Invariants — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 1.0  
**Last Updated**: 2026-10-17  

---

## 1. Sơ đồ Chỉ mục Tài liệu Kiến trúc (Architecture Index Map)

Tầng kiến trúc này là **Nguồn sự thật duy nhất (Single Source of Truth)** cho toàn bộ hệ thống kỹ thuật BAHA Ads Manager. Mọi nhà phát triển và AI Coding Agent bắt buộc phải tuân thủ nghiêm ngặt các nguyên tắc và ranh giới tại đây:

```
docs/architecture/
├── 01-system-context.md           ← Ranh giới hệ thống, Actors, Use Case Diagram, Workflow tổng thể
├── 02-high-level-architecture.md  ← Mô hình kiến trúc phân tầng (Client-Server), Topology hệ thống
├── 03-service-architecture.md     ← Kiến trúc phân lớp Router / Service / Repository phía Backend
├── 04-deployment-architecture.md  ← Triển khai chạy cục bộ (Localhost), cổng mạng, cấu hình .env
├── 05-data-architecture.md        ← Cấu trúc bảng SQLite (meta_sessions, ad_creation_runs), DDL SQL
├── 06-ai-architecture.md          ← Ranh giới phân hệ AI (Out-of-scope MVP, lộ trình tương lai)
├── 07-security-architecture.md    ← Bảo mật OAuth 2.0 (state CSRF), cô lập Token, an toàn ngân sách PAUSED
├── 08-integration-architecture.md ← Chuỗi 5 bước tạo tài nguyên Meta v20.0, quy đổi tiền tệ D-06
├── 09-design-principles.md        ← Quy chuẩn mã nguồn Clean Code, Simplicity First, xử lý lỗi
├── 10-folder-structure.md         ← Cấu trúc thư mục chuẩn mực toàn dự án (Frontend / Backend)
├── 11-frontend-system-design.md   ← Định tuyến phân tab, cấu trúc điều hướng SPA phía Client
├── 12-design-system.md            ← Thư viện thành phần UI dùng chung (Buttons, Badges, AdPreview)
├── 13-frontend-architecture.md    ← Quản lý trạng thái State Management & Singleton API Client
├── 14-design-language.md          ← Bảng màu nhận diện thương hiệu Meta/Enterprise, Spacing, Typography
└── adr/
    └── ADR-001.md                 ← Biên bản quyết định kiến trúc: Đánh đổi Tech stack & Pipeline MVP
```

---

## 2. Hệ thống Rào chắn Kiến trúc Bất biến (Architecture Guardrails Summary)

| Phân hệ | Tài liệu dẫn chiếu | Ràng buộc bất biến đối với Lập trình viên & AI Agent |
|---|---|---|
| **Cơ sở dữ liệu** | [05-data-architecture.md](05-data-architecture.md) | Chỉ sử dụng 2 bảng `meta_sessions` (duy nhất id=1) và `ad_creation_runs` (ID nullable). Tuyệt đối không thêm bảng hay đổi kiểu dữ liệu tùy tiện. |
| **Bảo mật & Token** | [07-security-architecture.md](07-security-architecture.md) | Không trả access token hoặc secret về frontend. Luôn xác thực `state` khi xử lý OAuth callback. |
| **An toàn ngân sách** | [07-security-architecture.md](07-security-architecture.md) | Tất cả chiến dịch tạo mới phải mặc định `status: "PAUSED"`. Không tự động retry khi gặp timeout. |
| **Định dạng & Tiền tệ** | [08-integration-architecture.md](08-integration-architecture.md) | Mục tiêu `OUTCOME_TRAFFIC`, Link Ad, CTA `LEARN_MORE`. Quy đổi ngân sách: nhân 100 với USD/EUR; giữ nguyên số nguyên với VND. |
| **Chuỗi API Meta** | [08-integration-architecture.md](08-integration-architecture.md) | Bắt buộc tuân thủ đúng trật tự: Image Hash $\rightarrow$ Campaign $\rightarrow$ Ad Set $\rightarrow$ Creative $\rightarrow$ Ad. |
| **Thư mục & Môi trường** | [10-folder-structure.md](10-folder-structure.md) | Phải dùng `.venv` cục bộ trong `backend/` và `node_modules` cục bộ trong `frontend/`. Không cài đặt thư viện vào global system. |
