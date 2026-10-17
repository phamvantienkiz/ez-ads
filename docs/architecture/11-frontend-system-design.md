# 11. Frontend System Design & Layout — "Soft Clean Cards"

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 2.0 (Grounded on Soft Clean Cards)  
**Last Updated**: 2026-10-17  
**Theme Mode**: Light Mode Only (MVP Scope)  

---

## 1. Canvas & Layout Structure

Giao diện **BAHA Ads Manager** tuân thủ cấu trúc bố cục phẳng, thoáng đãng và có trật tự thị giác cao:
- **Canvas Nền**: Nền tổng thể `--bg-page` (`#F5F5F7`), có dải gradient cực nhẹ chuyển dần sang xám `#EDEDF0` ở đáy trang web.
- **Container Căn giữa**: Toàn bộ nội dung nằm trong container căn giữa màn hình với chiều rộng tối đa `max-w-5xl` (~1024px - 1140px), đảm bảo bố cục tập trung hoàn hảo trên màn hình laptop của người thuyết trình.
- **Khoảng cách nhịp nhàng (Spacing)**: Khoảng cách giữa Header và các Cards là `28px - 32px`.

```
┌─────────────────────────────────────────────────────────────┐
│ Canvas: linear-gradient(180deg, #F5F5F7 70%, #EDEDF0 100%)  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ [Header Card]                                       │   │
│   │ BAHA Ads Manager · Status Pill · Connect Button    │   │
│   └─────────────────────────────────────────────────────┘   │
│                             │                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ [Global Asset Bar]                                  │   │
│   │ Segmented Tabs: [ Dashboard | Create Ad | Campaign ]│   │
│   │ Selectors: [ Ad Account Dropdown ] [ Page Dropdown ]│   │
│   └─────────────────────────────────────────────────────┘   │
│                             │                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ [Active Viewport Card] (Radius 28px, Shadow-card)   │   │
│   │ - Tab Dashboard: 3 Hero Metric Cards + Latest Run   │   │
│   │ - Tab Create Ad: 2-Column Grid (Form + Live Preview)│   │
│   │ - Tab Campaigns: Minimal Borderless Table + Refresh │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Layout Chi tiết cho Từng Tab Chức năng

### 2.1. Tab 1: Dashboard Vận hành
Thiết kế theo chuẩn **Hàng chỉ số (Metric Row)** với con số lớn làm điểm nhấn thị giác (Hero):
- **Khối Hero 1**: Trạng thái kết nối Meta (Pill xanh "Đã kết nối" + tài khoản đăng nhập).
- **Khối Hero 2**: Số lượng chiến dịch hiện có (`Display 48px`, font tabular, nhãn xám nhỏ "Chiến dịch trên Ad Account").
- **Khối Hero 3**: Trạng thái tài nguyên tạo gần nhất (Thẻ kết quả phiên chạy với 4 ID thật từ Meta).

### 2.2. Tab 2: Tạo Quảng cáo Sản phẩm (Create Ad)
Bố cục lưới 2 cột tỷ lệ `7 : 5` trên Desktop:
- **Cột Trái (7 phần)**: Form nhập liệu tối giản trong card trắng, bao gồm:
  - Tiêu đề card: "Tạo chiến dịch mới" (`title-lg 28px`).
  - Các ô input bo góc 12px trên nền `subtle`.
  - Cảnh báo an toàn ngân sách mặc định `status: PAUSED`.
  - Nút Primary "Xác nhận tạo quảng cáo trên Meta" màu đen `--ink`.
- **Cột Phải (5 phần)**: Vùng dán dính (Sticky) chứa thẻ xem trước bài viết Facebook (`AdPreviewCard`), tự động cập nhật nội dung khi người dùng gõ vào form.

### 2.3. Tab 3: Danh sách Chiến dịch (Campaigns)
- Bảng dữ liệu phẳng, tối giản, **không có viền cứng**, không nền xen kẽ.
- Hàng tiêu đề nhãn mờ `label` (`text-muted`).
- Các hàng chiến dịch cách nhau bằng đường kẻ mờ 1px `border-hairline`.
- Nút "Làm mới dữ liệu" (Refresh) dạng icon tròn nhỏ 32x32 với `--shadow-control` ở góc trên bên phải card.

---

## 3. Quy chuẩn Điều hướng & Tương tác

- **Tab Switching**: Sử dụng **Segmented Control** nền `subtle` bo góc 16px. Khi bấm chuyển tab, nền trắng bo góc 12px trượt mượt mà trong `200ms`.
- **Responsive Behavior**:
  - Desktop ($\ge 1024px$): Hiển thị đầy đủ 2 cột song song (Form bên trái, Preview bên phải).
  - Tablet/Mobile ($< 1024px$): Tự động xếp chồng cột (Form ở trên, Preview ở dưới).
