# Software Requirements Specification (SRS) — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Tài liệu tham chiếu**: [prd.md](prd.md)  
**Ngày phê duyệt**: 2026-10-17  
**Trạng thái**: Approved  

---

## 1. Scope & System Purpose

Tài liệu này xác định chi tiết các đặc tả yêu cầu phần mềm và các ràng buộc phi chức năng (Non-Functional Requirements - NFR) cho phiên bản **Release 1: MVP Demo**, bảo đảm hệ thống vận hành ổn định trong buổi trình diễn 2 giờ.

---

## 2. Non-Functional Requirements (NFR) Specifications

### NFR-01: Bảo mật & Cô lập Bí mật (Security & Secret Isolation)
- **Ràng buộc**: `META_APP_SECRET` chỉ tồn tại trong backend environment. Không bao giờ commit vào Git.
- **Client Shielding**: Không trả access token hoặc App Secret về frontend trong bất kỳ response nào.
- **Log Privacy**: Không log access token, mã authorization code, hoặc toàn bộ URL callback chứa code vào console/file logs.
- **State Validation**: Bắt buộc xác minh tham số `state` tại OAuth callback; từ chối mọi request không khớp state để chống tấn công CSRF.

### NFR-02: Tính trung thực của Dữ liệu (Data Authenticity)
- **Ràng buộc cốt lõi**: 100% dữ liệu hiển thị (Ad Accounts, Pages, Campaigns, Resource IDs) phải được truy vấn trực tiếp từ Meta Graph/Marketing API.
- **Cấm giả lập (No Fake Mocks)**: Tuyệt đối không tạo nút "Thành công giả" hay hiển thị ID tự sinh mà không gọi API thật của Meta.
- **Phản ánh trung thực**: Nếu tài khoản thiếu quyền, thiếu phương thức thanh toán hoặc API lỗi, hệ thống phải báo đúng lỗi đó.

### NFR-03: Hiệu năng & Giới hạn Thời gian (Performance & Timeouts)
- **Thời gian phản hồi cục bộ**: Các endpoint nội bộ (`/api/health`, `/api/meta/status`) phải phản hồi trong `< 50ms`.
- **Độ trễ tích hợp Meta**: Chuỗi 5 lời gọi Meta Marketing API phải có tổng thời gian thực thi `< 10s` trong điều kiện mạng bình thường.
- **Client Timeout**: Cấu hình `timeout = 30.0s` cho HTTP client (`httpx`) khi gọi sang máy chủ Meta.

### NFR-04: Khả năng vận hành & Cài đặt (Operational Simplicity)
- **Môi trường độc lập**: Sử dụng môi trường ảo Python (`.venv`) và thư mục `node_modules` cục bộ, không can thiệp vào cấu hình hệ thống máy chủ.
- **Tự động khởi tạo DB**: Ứng dụng tự động kiểm tra và khởi tạo các bảng SQLite khi backend khởi động nếu tệp DB chưa tồn tại.
- **Thông báo lỗi rõ ràng**: Nếu thiếu biến môi trường cấu hình Meta, backend phải báo rõ biến nào bị thiếu thay vì crash đột ngột.
