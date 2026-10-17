# 09. Design Principles & Code Standards — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 1.0  
**Last Updated**: 2026-10-17  

---

## 1. Core Engineering Principles (Bám sát AGENTS.md)

1. **Simplicity First (Đơn giản là trên hết)**:
   - Viết lượng code tối thiểu giải quyết triệt để bài toán. Tuyệt đối không thêm tính năng suy diễn hoặc cấu trúc "phòng bị tương lai".
   - Không thêm tầng trung gian trừu tượng (AbstractFactory, GenericUoW...) khi chưa có 3 đối tượng kế thừa cụ thể.
2. **Surgical Changes (Thay đổi chuẩn xác, phẫu thuật)**:
   - Chỉ chỉnh sửa những dòng code liên quan trực tiếp đến yêu cầu. Không tự tiện format lại code hoặc đổi tên biến xung quanh.
3. **Fail Explicitly, Zero Silent Failures (Xử lý lỗi tường minh)**:
   - Mọi exception từ Meta API hoặc truy vấn DB phải được bắt, ghi log cảnh báo an toàn và phản hồi về client với mã lỗi xác định. Không dùng `except Exception: pass`.
4. **No Hidden Logs (Không để lọt log rác)**:
   - Không commit các lệnh `console.log` hoặc `print()` debug tạm bợ. Sử dụng logging chuẩn của Python (`logger.info`, `logger.error`).

---

## 2. Backend Design Standards (FastAPI + Python)

- **PEP 8 Compliance**: Đặt tên hàm và biến dạng `snake_case`, tên lớp dạng `PascalCase`, hằng số dạng `UPPER_CASE`.
- **Type Hinting**: 100% các hàm nghiệp vụ và endpoints phải có type annotations đầy đủ cho tham số đầu vào và kiểu trả về.
- **Async/Await**: Sử dụng `async def` cho các router handler và lời gọi I/O không đồng bộ với `httpx.AsyncClient` và `aiosqlite`.
- **Validation**: Mọi dữ liệu request payload gửi lên backend phải được validate qua **Pydantic V2 BaseModel**.

---

## 3. Frontend Design Standards (Next.js + TypeScript + Tailwind)

- **Strict TypeScript**: Cấm sử dụng kiểu `any` trừ khi không thể tránh khỏi khi tương tác với thư viện bên ngoài chưa có type definitions.
- **Component Modularity**: Mỗi component giao diện chỉ đảm nhận một trách nhiệm duy nhất (Single Responsibility Principle):
  - `ConnectCard`: Trạng thái và nút kết nối Meta.
  - `AssetSelector`: Dropdown chọn Ad Account và Fanpage.
  - `AdForm`: Biểu mẫu nhập thông tin sản phẩm.
  - `AdPreviewCard`: Thẻ mô phỏng bài quảng cáo.
  - `CampaignTable`: Bảng hiển thị danh sách chiến dịch thật.
- **Utility-First Styling**: 100% giao diện được dựng bằng Tailwind CSS, không viết file CSS tùy biến rời rạc.
