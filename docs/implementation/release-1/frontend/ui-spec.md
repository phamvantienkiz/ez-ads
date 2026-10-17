# UI Specification & Screen Design — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Phong cách thiết kế**: "Soft Clean Cards" (Light Mode Only)  
**Tài liệu tham chiếu**: [soft-clean-cards.md](../../../requirement/soft-clean-cards.md), [12-design-system.md](../../../architecture/12-design-system.md), [14-design-language.md](../../../architecture/14-design-language.md)  
**Ngày cập nhật**: 2026-10-17  
**Trạng thái**: Approved & Ready for Frontend Dev  

---

## 1. Tổng quan Giao diện & Layout Canvas

Ứng dụng **BAHA Ads Manager** được thiết kế dưới dạng Single Page Application (SPA) gồm một canvas căn giữa màn hình với nền gradient nhẹ `linear-gradient(180deg, #F5F5F7 70%, #EDEDF0 100%)`.

### Cấu trúc Khung màn hình:
1. **Header Bar**: Logo thương hiệu, Pill trạng thái kết nối Meta và nút Connect / Disconnect.
2. **Asset Navigation Bar**: Thanh điều hướng phân tab dạng Segmented Control + 2 dropdown chọn Ad Account & Fanpage.
3. **Card Nội dung Động**:
   - Màn hình 1: **Dashboard Vận hành** (Cards chỉ số & kết quả chạy gần nhất).
   - Màn hình 2: **Tạo Quảng cáo Sản phẩm** (Lưới 2 cột: Form nhập liệu + Live Ad Preview).
   - Màn hình 3: **Danh sách Chiến dịch** (Bảng dữ liệu Meta thật kèm nút Refresh).

---

## 2. Chi tiết Thiết kế Từng Màn hình (Screen Specifications)

### 2.1. Header Bar & Trạng thái Kết nối Meta

- **Vị trí**: Cố định phía trên cùng của container nội dung.
- **Thành phần**:
  - Bên trái: Tên ứng dụng `BAHA Ads Manager` (`title-md 18px`, font chữ đen đậm `#0B0B0F`).
  - Bên phải:
    - Nếu **Chưa kết nối**: Hiển thị nút bấm `Connect Facebook` màu xanh `#1F5FFF`, bo tròn `999px`, icon Facebook trắng, đổ bóng `shadow-control`.
    - Nếu **Đã kết nối**: Hiển thị Pill badge nền mint `#D8F3E4`, chấm tròn xanh `#1FA63A`, chữ "Đã kết nối Meta", và nút nhỏ "Ngắt kết nối" dạng text mờ xám.

---

### 2.2. Thanh Chọn Tài sản & Điều hướng Tab (Asset & Nav Bar)

- **Segmented Tabs**:
  - Khung xám nhạt `#F4F4F6`, bo góc `16px`, padding `4px`.
  - 3 tabs: **Tổng quan (Dashboard)**, **Tạo quảng cáo (Create Ad)**, **Chiến dịch (Campaigns)**.
  - Tab đang chọn có nền trắng `#FFFFFF`, bo góc `12px`, chữ đen `#0B0B0F`, bóng `shadow-control`.
- **Dropdowns Lựa chọn Tài sản**:
  - `Ad Account Selector`: Dropdown hiển thị Tên tài khoản + Account ID + Currency (VND/USD).
  - `Facebook Page Selector`: Dropdown hiển thị Tên Fanpage + Page ID.
  - Cả hai dropdown dùng nền `#FFFFFF`, viền mờ `1px solid #E9E9EE`, bo góc `12px`.

---

### 2.3. Màn hình 1: Dashboard Vận hành (Tab "Dashboard")

Áp dụng nguyên tắc **"Con số là nhân vật chính"**:
- **Khối 1: Thống kê Chiến dịch**:
  - Card bo góc `28px`, nền trắng, bóng `shadow-card`.
  - Nhãn: `Chiến dịch trên Ad Account` (`label 13px`, màu xám `#6B6B76`).
  - Số hiển thị: Số lượng chiến dịch hiện có (`Display 48px`, font tabular, ví dụ: `12`).
- **Khối 2: Kết quả Phiên Tạo Gần Nhất (Latest Creation Run)**:
  - Nếu **Chưa có phiên chạy nào**: Hiển thị empty state nền `#F4F4F6`, chữ xám: "Chưa có lượt tạo quảng cáo nào trong phiên này."
  - Nếu **Đã có kết quả**: Hiển thị Card chi tiết với:
    - Huy hiệu trạng thái: `Thành công` (Xanh lá `#1FA63A`) hoặc `Thất bại một phần` (Đỏ `#E5483D`).
    - Lưới 4 ô hiển thị các ID thật:
      - `Campaign ID`: `120210000000001`
      - `Ad Set ID`: `120210000000002`
      - `Creative ID`: `120210000000003`
      - `Ad ID`: `120210000000004`
    - Nhãn chú thích: Mọi tài nguyên đều ở trạng thái `PAUSED` an toàn.

---

### 2.4. Màn hình 2: Tạo Quảng cáo Sản phẩm (Tab "Create Ad")

Bố cục 2 cột song song (Grid 12 cột: Cột trái 7 phần, Cột phải 5 phần):

#### Cột Trái: Biểu mẫu Nhập liệu (Ad Form Card)
- Card trắng bo góc `28px`, padding `24px`, bóng `shadow-card`.
- Tiêu đề: `Tạo quảng cáo sản phẩm mới` (`title-lg 28px`, font-medium).
- Các trường nhập liệu (Input bo góc `12px`, nền `#F4F4F6`, hover `#ECECEF`):
  1. **Tên chiến dịch** (`campaignName`): Placeholder "Ví dụ: BAHA Polo Shirt Traffic Campaign".
  2. **Ngân sách hàng ngày** (`budgetAmount`): Điền số tiền, bên cạnh tự động hiển thị đơn vị tiền tệ của Ad Account (VND / USD).
  3. **Tiêu đề bài viết** (`headline`): Tiêu đề hiển thị dưới ảnh Link Ad.
  4. **Nội dung chính** (`primaryText`): Khung textarea 3 dòng.
  5. **URL trang đích sản phẩm** (`destinationUrl`): Bắt buộc kiểm tra định dạng `http/https`.
  6. **URL hình ảnh sản phẩm** (`imageUrl`): Link ảnh công khai để Meta băm hash.
- **Hộp Cảnh báo An toàn Ngân sách**:
  - Khung màu vàng nhạt `#FFF1C9` bo góc `12px`, viền `#FFE494`.
  - Icon khiên bảo vệ + thông báo: "Chiến dịch sẽ được tạo ở trạng thái TẠM DỪNG (PAUSED). Hệ thống không tự động kích hoạt chi tiêu quảng cáo."
- **Nút Xác nhận Submit (Primary Ink Button)**:
  - Nền đen `#111114`, chữ trắng, bo góc `12px`, padding cao `48px`, font-medium `14px`.
  - Văn bản: "Xác nhận tạo quảng cáo trên Meta".
  - Khi đang gửi: Nút chuyển sang trạng thái disabled + Spinner xoay vòng.

#### Cột Phải: Trình Xem Trước Trực Quan (Live Ad Preview Card)
- Vùng dán dính (Sticky) bám theo màn hình khi cuộn chuột.
- Khung xám nhạt `#F4F4F6` bo góc `24px`, padding `20px`.
- Bên trong chứa thẻ mô phỏng **Facebook Feed Link Ad Card**:
  - Header: Avatar tròn Fanpage + Tên Fanpage + nhãn "Được tài trợ".
  - Body text: Hiển thị thời gian thực theo trường `primaryText` người dùng đang gõ.
  - Image box: Khung ảnh tỷ lệ `1.91:1` hiển thị ảnh từ `imageUrl`.
  - Link bar: Domain sản phẩm + `headline` in đậm + nút trắng nhỏ "Tìm hiểu thêm".

---

### 2.5. Màn hình 3: Danh sách Chiến dịch (Tab "Campaigns")

- Card trắng bo góc `28px`, padding `24px`, bóng `shadow-card`.
- Tiêu đề: `Danh sách chiến dịch trên Meta` (`title-lg 28px`).
- Góc phải: Nút icon tròn `32x32px` "Làm mới dữ liệu" (Refresh) với bóng `shadow-control`.
- **Bảng dữ liệu tối giản**:
  - Không có viền dọc, không có nền xen kẽ sọc ngựa vằn.
  - Các cột:
    - **Tên chiến dịch**: Chữ đen đậm `body 14px`.
    - **Campaign ID**: Chữ xám font `tabular-nums` `value 13px`.
    - **Mục tiêu**: `OUTCOME_TRAFFIC`.
    - **Trạng thái**: Pill badge vàng nhạt `#FFF1C9` với chấm tròn cam `#FF8A1F` cho `PAUSED`.
    - **Ngày tạo**: Chữ xám mờ `caption 12px`.
  - Giữa các hàng: Đường kẻ mờ 1px `#EFEFF2`.
- **Empty State**: Nếu tài khoản chưa có chiến dịch, hiển thị minh họa tối giản và nút chuyển sang tab Tạo quảng cáo.

---

## 3. Micro-Interactions & Animation Guidelines

- **Thời lượng tương tác nút**: `120ms ease-out` khi hover và active `scale(0.98)`.
- **Chuyển tab Segmented**: `200ms cubic-bezier(0.32, 0.72, 0, 1)` với hiệu ứng trượt nền trắng.
- **Tuyệt đối cấm**:
  - Không sử dụng hiệu ứng rơi/bay trang trí rườm rà.
  - Không dùng dark mode trong bản demo MVP (chỉ tập trung hoàn thiện 1 light mode chuẩn mực).
