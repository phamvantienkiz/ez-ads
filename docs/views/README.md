# Visual Views & Interactive Artifacts Index (`docs/views/`)

**Tầng tài liệu**: Visual Views (Standalone HTML Artifacts)  
**Nguyên tắc quản trị**: Pure Markdown Core & Centralized On-Demand HTML Views  
**Ngày cập nhật**: 2026-10-17  

---

## 1. Mục đích Thư mục

Thư mục `docs/views/` là nơi lưu trữ tập trung các tệp **HTML trực quan độc lập (Self-contained Single-File HTML Artifacts)** như sơ đồ kiến trúc tương tác, bản mẫu giao diện (interactive prototypes/wireframes), hoặc bảng trình chiếu kỹ thuật khi có yêu cầu xuất bản trực quan.

## 2. Quy tắc Bất biến (Invariants)

1. **Tách biệt hoàn toàn với tài liệu cốt lõi**: Toàn bộ tài liệu trong `docs/business/`, `docs/architecture/` và `docs/implementation/` bắt buộc giữ định dạng **Pure Markdown (`.md`)** và sơ đồ **Mermaid** thuần túy. Mọi tệp HTML tương tác chỉ được đặt tại `docs/views/`.
2. **Khởi tạo theo yêu cầu (On-Demand Only)**: Chỉ sinh các tệp `.html` trong thư mục này khi có yêu cầu rõ ràng từ người dùng (không tự động sinh dư thừa trong quá trình viết tài liệu nghiệp vụ hoặc code MVP 2 giờ).
3. **Nguồn sự thật duy nhất (Single Source of Truth)**: Mọi tệp visual view tại đây chỉ đóng vai trò biểu diễn trực quan từ dữ liệu gốc tại `docs/architecture/` và `docs/implementation/release-1/`.

---

## 3. Danh mục Hiện tại

*(Hiện tại chưa có tệp HTML view nào được yêu cầu khởi tạo cho Release 1 MVP Demo — toàn bộ sơ đồ hệ thống đang được nhúng trực tiếp bằng chuẩn Mermaid trong các tài liệu Markdown gốc).*
