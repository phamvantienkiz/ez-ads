# Stakeholder Register & Decision Authority (RACI) — BAHA Ads Manager

**Document Layer**: Business Layer  
**Version**: 1.0  
**Date**: 2026-10-17  
**Status**: Active  

---

## 1. Stakeholder Register

| Vai trò / Chức danh | Tên đại diện | Nhóm bên liên quan | Trách nhiệm chính trong dự án |
|---|---|---|---|
| **Sponsor / Business Owner** | BAHA Leadership | Nội bộ BAHA | Định hướng chiến lược, cung cấp tài nguyên, phê duyệt phạm vi MVP và đánh giá kết quả demo. |
| **Demo Operator / User** | Chuyên viên BAHA | Người dùng trực tiếp | Thực hiện đăng nhập Facebook, chọn Ad Account/Page, điền form quảng cáo và xác nhận tạo chiến dịch trong buổi demo. |
| **Technical Lead / Architect** | Lead Engineer | Đội ngũ phát triển | Quyết định kiến trúc hệ thống, lựa chọn tech stack, bảo đảm tính an toàn bảo mật token và tính toàn vẹn của API contract. |
| **Fullstack Engineer** | Dev Team / Antigravity | Đội ngũ phát triển | Hiện thực hóa mã nguồn (FastAPI + Next.js + SQLite), xử lý tích hợp Meta Marketing API và tối ưu luồng chạy 2 giờ. |
| **External Platform Partner** | Meta Platforms Inc. | Đối tác nền tảng bên thứ ba | Cung cấp hạ tầng Meta Graph API, Marketing API, OAuth Login và tiếp nhận yêu cầu tạo tài nguyên quảng cáo. |

---

## 2. RACI Matrix cho các hoạt động chính

- **R (Responsible)**: Người trực tiếp thực hiện công việc.
- **A (Accountable)**: Người chịu trách nhiệm phê duyệt cuối cùng.
- **C (Consulted)**: Người được tham vấn ý kiến chuyên môn.
- **I (Informed)**: Người được thông báo kết quả.

| Hoạt động dự án | Business Owner | Demo Operator | Tech Lead | Fullstack Dev | Meta Platform |
|---|:---:|:---:|:---:|:---:|:---:|
| Thống nhất phạm vi MVP & Tiêu chí Demo | **A** | **C** | **C** | **R** | **I** |
| Cung cấp tài khoản Facebook, Ad Account & Page | **A** | **R** | **I** | **I** | **I** |
| Cấu hình Meta App (App ID, Secret, Scopes, Redirect URI) | **I** | **I** | **A** | **R** | **C** |
| Phê duyệt kiến trúc kỹ thuật & thiết kế API | **I** | **I** | **A** | **R** | **I** |
| Hiện thực hóa mã nguồn và kết nối API | **I** | **I** | **A** | **R** | **C** |
| Thực hiện buổi Demo kiểm chứng End-to-End | **A** | **R** | **C** | **C** | **I** |
