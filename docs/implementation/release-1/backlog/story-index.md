# Backlog Sổ cái — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Nguồn tham chiếu PRD**: [prd.md](../prd.md)  
**Sơ đồ luồng & Context**: [01-system-context.md](../../../architecture/01-system-context.md)  
**Ngày cập nhật**: 2026-10-17  
**Trạng thái**: Approved & Ready for Implementation  

---

## 1. Ma trận phân rã User Story & Traceability

| Mã Story | Tiêu đề User Story | Persona | Ưu tiên | PRD FR Ref | Số AC | Architecture Guardrails | Trạng thái |
|---|---|---|:---:|:---:|:---:|---|:---:|
| **[US-001](stories/US-001.md)** | Kết nối Facebook qua Meta OAuth và duy trì phiên | BAHA Demo Operator | P0 | FR-01, FR-09 | 4 ACs | 05-data (`meta_sessions`), 07-security (CSRF `state`, token isolation) | Ready for Dev |
| **[US-002](stories/US-002.md)** | Tải và chọn Tài khoản quảng cáo (Ad Account) | BAHA Demo Operator | P0 | FR-02 | 3 ACs | 07-security (Token pass-through), 08-integration (Meta Graph API) | Ready for Dev |
| **[US-003](stories/US-003.md)** | Tải và chọn Facebook Fanpage đại diện | BAHA Demo Operator | P0 | FR-03 | 3 ACs | 07-security (Page permissions), 08-integration (Meta Graph API) | Ready for Dev |
| **[US-004](stories/US-004.md)** | Biểu mẫu nhập thông tin quảng cáo & quy đổi tiền tệ | BAHA Demo Operator | P0 | FR-04 | 4 ACs | 08-integration (Currency multiplier rule, targeting invariants) | Ready for Dev |
| **[US-005](stories/US-005.md)** | Xem trước bài quảng cáo và xác nhận an toàn | BAHA Demo Operator | P0 | FR-05 | 3 ACs | 07-security (Safe default `PAUSED`, no auto-spend) | Ready for Dev |
| **[US-006](stories/US-006.md)** | Điều phối chuỗi 5 lời gọi Meta API tạo tài nguyên | Backend / System | P0 | FR-06 | 5 ACs | 05-data (`ad_creation_runs`), 07-security (Sanitized errors, partial failure) | Ready for Dev |
| **[US-007](stories/US-007.md)** | Truy vấn và hiển thị danh sách chiến dịch thật | BAHA Demo Operator | P0 | FR-07 | 3 ACs | 08-integration (Meta Marketing API, empty state, data integrity) | Ready for Dev |
| **[US-008](stories/US-008.md)** | Bảng điều khiển tối giản & quản lý trạng thái tải/lỗi | BAHA Demo Operator | P0 | FR-08, FR-09 | 4 ACs | 09-design-principles (Consistent envelope, double-submit lock) | Ready for Dev |

---

## 2. Thống kê độ bao phủ kiểm thử (Test Coverage Matrix)

- **Tổng số User Stories**: 8 stories.
- **Tổng số Acceptance Criteria**: 29 scenarios.
  - **Happy Path (Thành công chuẩn)**: 8 scenarios (100% các story có luồng chính).
  - **Validation & Edge Cases (Điều kiện biên / Dữ liệu rỗng)**: 11 scenarios (xử lý danh sách rỗng, đơn vị tiền tệ, form validation).
  - **Negative & Failure Paths (Nhánh lỗi bên thứ ba / Partial Failure)**: 10 scenarios (từ chối cấp quyền OAuth, lỗi Meta API từng bước, timeout mạng).

---

## 3. Danh mục Quyết định Kỹ thuật (Technical Decisions) & Câu hỏi mở (OQ)

| Mã | Nội dung | Trạng thái | Ghi chú giải quyết |
|---|---|:---:|---|
| `D-01` | Mục tiêu quảng cáo: `OUTCOME_TRAFFIC`, Định dạng: `Single Image Link Ad`, Trạng thái mặc định: `PAUSED`. | `[x] Resolved` | Đã chốt trong PRD, ánh xạ vào US-004, US-005, US-006. |
| `D-02` | Tải ảnh bằng URL công khai qua endpoint `/adimages` lấy `image_hash`. | `[x] Resolved` | Ánh xạ vào US-004 và US-006. |
| `D-03` | Cố định targeting tối thiểu: Toàn quốc VN, 18-65 tuổi, All genders. | `[x] Resolved` | Ánh xạ vào US-004 và US-005. |
| `D-04` | Meta App Development Mode, Redirect URI: `http://localhost:8000/api/meta/callback`. | `[x] Resolved` | Ánh xạ vào US-001. |
| `D-05` | Lưu access token vào SQLite `meta_sessions` (duy nhất id=1). | `[x] Resolved` | Ánh xạ vào US-001. |
| `D-06` | Quy đổi ngân sách: nhân 100 với USD/EUR; giữ nguyên số nguyên với VND. | `[x] Resolved` | Ánh xạ vào US-004. |
| `OQ-01` | *Không còn câu hỏi mở tồn đọng cho Release 1 (Toàn bộ 6 quyết định kỹ thuật đã chốt).* | `[x] Closed` | Đủ điều kiện bắt tay vào lập trình. |
