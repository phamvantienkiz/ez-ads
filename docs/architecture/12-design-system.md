# 12. Design System & Component Library Specs — "Soft Clean Cards"

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 2.0 (Grounded on Soft Clean Cards)  
**Last Updated**: 2026-10-17  

---

## 1. Triết lý Thiết kế Component

Toàn bộ các thành phần giao diện của **BAHA Ads Manager** được thiết kế nhất quán theo hệ chuẩn **Soft Clean Cards**:
- **Không đặt Card lồng trong Card**: Thay vào đó, dùng vùng phụ `--bg-subtle` (`#F4F4F6`) với bo góc 12px hoặc 16px để tạo phân cấp bên trong card chính.
- **Tập trung vào tương phản mờ**: Viền 1px mờ nhạt (`#E9E9EE`), bóng đổ lan tỏa mờ mịn, không có viền đen thô ráp.
- **Độ nhạy tương tác (Micro-interactions)**: Mọi thao tác hover và click đều phản hồi nhanh (120ms - 200ms) với hiệu ứng scale nhẹ hoặc đổi sắc độ xám.

---

## 2. Thông số Chi tiết của các Component Cốt lõi

### 2.1. Card Chức năng Chính (`Card.tsx`)
Khung chứa cơ sở cho từng khối nhiệm vụ (Header, Form, Preview, Campaigns):

```tsx
// Structure & Classes
<div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col gap-5">
  {children}
</div>
```

- **Background**: `#FFFFFF` (`--bg-card`)
- **Border**: `1px solid #E9E9EE` (`--border-card`)
- **Border Radius**: `28px` (`--radius-xl` / `rounded-card`)
- **Padding**: `24px` (`p-6`)
- **Box Shadow**: `0 1px 2px rgba(16, 16, 24, 0.04), 0 8px 24px rgba(16, 16, 24, 0.06)`

---

### 2.2. Thanh Điều hướng Phân tab (`SegmentedControl.tsx`)
Dùng để chuyển đổi giữa 3 màn hình chính: **Dashboard**, **Tạo quảng cáo (Create Ad)**, và **Chiến dịch (Campaigns)**.

```tsx
<div className="bg-subtle rounded-2xl p-1 inline-flex gap-1 border border-border-hairline">
  <button
    className={`px-4 py-2 rounded-xl text-[13px] font-medium transition-all duration-200 ${
      isActive
        ? "bg-white text-primary shadow-control"
        : "text-muted hover:text-primary"
    }`}
  >
    {tabLabel}
  </button>
</div>
```

- **Container**: Nền `--bg-subtle` (`#F4F4F6`), bo góc `16px`, padding `4px`.
- **Active Tab Button**: Nền `#FFFFFF`, chữ `--text-primary` (`#0B0B0F`), bo góc `12px`, bóng `--shadow-control` (`0 1px 2px rgba(16, 16, 24, 0.08)`).
- **Inactive Tab Button**: Không nền, chữ `--text-secondary` (`#6B6B76`), hover sáng nhẹ.

---

### 2.3. Nút Hành động Chính (`PrimaryButton.tsx` — Nút Ink)
Dành riêng cho hành động then chốt nhất trên mỗi card (ví dụ: "Xác nhận tạo quảng cáo trên Meta").

```tsx
<button className="bg-ink hover:bg-black text-white text-[14px] font-medium px-5 py-3 rounded-xl shadow-primary transition-all duration-150 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
  {isLoading ? <Spinner className="w-4 h-4 text-white" /> : label}
</button>
```

- **Background**: `#111114` (`--ink`)
- **Text**: `#FFFFFF`, font-weight `500`
- **Border Radius**: `12px` (`--radius-md`)
- **Shadow**: `0 6px 16px rgba(16, 16, 24, 0.22)`
- **Hover / Active**: `hover:bg-black`, `active:scale-[0.98]`

---

### 2.4. Nút Kết nối Meta (`MetaConnectButton.tsx`)
Dùng riêng cho thao tác kết nối OAuth Facebook:

```tsx
<button className="bg-[#1F5FFF] hover:bg-[#1850DE] text-white text-[13px] font-medium px-4 py-2 rounded-full shadow-control flex items-center gap-2 transition-all">
  <FacebookIcon className="w-4 h-4" />
  Connect Facebook
</button>
```

- **Background**: `#1F5FFF` (`--data-1`)
- **Border Radius**: `999px` (`--radius-full`)
- **Shadow**: `--shadow-control`

---

### 2.5. Trạng thái & Huy hiệu (`StatusBadge.tsx`)
Hiển thị trạng thái kết nối và trạng thái chiến dịch (`PAUSED`, `ACTIVE`, `Connected`):

```tsx
// Pill Badge chuẩn Soft Clean
<span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[12px] font-medium ${badgeStyle}`}>
  <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: dotColor }} />
  {label}
</span>
```

| Trạng thái | Nền Badge | Màu chữ & Chấm tròn | Ý nghĩa |
|---|---|---|---|
| **Connected** | `#D8F3E4` (Mint pastel) | `#1FA63A` (`--data-4`) | Đã kết nối Meta thành công |
| **Disconnected** | `#F4F4F6` (Subtle) | `#6B6B76` (`--text-secondary`) | Chưa kết nối |
| **PAUSED** | `#FFF1C9` (Yellow pastel) | `#FF8A1F` (`--data-3`) | Chiến dịch tạm dừng (mặc định an toàn) |
| **Error / Failed** | `#FFD9E8` (Pink pastel) | `#E5483D` (`--data-alert`) | Lỗi Meta API hoặc Partial Failure |

---

### 2.6. Ô Nhập liệu & Dropdown (`InputField.tsx`, `SelectField.tsx`)
Thiết kế phẳng, tinh tế, viền mờ nhạt:

```tsx
<div className="flex flex-col gap-1.5">
  <label className="text-[13px] text-muted">{label}</label>
  <input
    className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft"
    {...props}
  />
</div>
```

---

### 2.7. Thẻ Xem trước Bài quảng cáo (`AdPreviewCard.tsx`)
Mô phỏng chân thực bài quảng cáo Link Ad trên nền container `--bg-subtle`:

```tsx
<div className="bg-subtle rounded-2xl p-4 border border-border-hairline flex flex-col gap-3 max-w-[380px]">
  {/* Header: Page Avatar + Name */}
  <div className="flex items-center gap-2.5">
    <div className="w-8 h-8 rounded-full bg-[#D9E8FF] flex items-center justify-center text-[12px] font-semibold text-[#1F5FFF]">
      {pageName ? pageName[0] : 'P'}
    </div>
    <div className="flex flex-col">
      <span className="text-[13px] font-medium text-primary leading-tight">{pageName || "Tên Facebook Page"}</span>
      <span className="text-[11px] text-muted-soft">Được tài trợ · Sponsored</span>
    </div>
  </div>

  {/* Primary Text */}
  <p className="text-[13px] text-primary leading-relaxed whitespace-pre-wrap">
    {primaryText || "Nội dung văn bản chính của bài quảng cáo sẽ hiển thị ở đây..."}
  </p>

  {/* Image Container */}
  <div className="w-full aspect-[1.91/1] bg-white rounded-xl overflow-hidden border border-border-hairline relative">
    {imageUrl ? (
      <img src={imageUrl} alt="Ad Preview" className="w-full h-full object-cover" />
    ) : (
      <div className="w-full h-full flex items-center justify-center text-muted-soft text-[12px]">
        Xem trước hình ảnh
      </div>
    )}
  </div>

  {/* Link & CTA Bar */}
  <div className="flex items-center justify-between pt-1">
    <div className="flex flex-col overflow-hidden pr-2">
      <span className="text-[12px] text-muted truncate">{domainName || "baha.vn"}</span>
      <span className="text-[13px] font-medium text-primary truncate">{headline || "Tiêu đề bài viết"}</span>
    </div>
    <span className="bg-white border border-border-card px-3 py-1.5 rounded-lg text-[12px] font-medium text-primary shadow-control shrink-0">
      Tìm hiểu thêm
    </span>
  </div>
</div>
```

---

### 2.8. Hàng Chỉ số Thống kê (`MetricBlock.tsx`)
Triết lý: Con số lớn là nhân vật chính, đơn vị và nhãn đi kèm yên lặng bên cạnh:

```tsx
<div className="flex flex-col">
  <span className="text-[13px] text-muted mb-1">{label}</span>
  <div className="flex items-baseline gap-2">
    <span className="text-[36px] font-normal tracking-tight text-primary font-tabular leading-none">{value}</span>
    {unit && <span className="text-[14px] text-muted">{unit}</span>}
  </div>
</div>
```
