# 14. Design Language & Tokens — "Soft Clean Cards" Style

**Document Layer**: Architecture Layer  
**Status**: Living Architecture (Single Source of Truth)  
**Version**: 2.0 (Grounded on Soft Clean Cards)  
**Last Updated**: 2026-10-17  
**Theme Mode**: Light Mode Only (MVP Scope)  

---

## 1. Triết lý Thiết kế Cốt lõi (Design Philosophy)

Giao diện **BAHA Ads Manager** được xây dựng dựa trên hệ quy chuẩn thiết kế **"Soft Clean Cards"**:
1. **Một thẻ = Một nhiệm vụ (One card = one mission)**: Mỗi card trả lời đúng một câu hỏi hoặc thực hiện một khối chức năng độc lập (Trạng thái kết nối, Chọn tài sản, Tạo chiến dịch, Danh sách chiến dịch).
2. **Con số/Tiêu đề là nhân vật chính**: Một phần tử lớn làm điểm nhấn thị giác, mọi thứ còn lại giữ kích thước nhỏ và yên lặng.
3. **Màu sắc là thông tin, không phải trang trí**: Toàn bộ UI giữ nền trắng – xám tối giản; màu sắc chỉ xuất hiện ở dữ liệu thật, trạng thái vận hành, và nút hành động chính.
4. **Khoảng trắng hào phóng (Generous Whitespace)**: Khoảng trống rộng rãi giúp mắt người dùng dễ dàng định vị các thông số quan trọng khi demo.
5. **Phân cấp bằng cỡ chữ và độ xám**: Tuyệt đối không dùng viền đậm, không dùng màu sắc lòe loẹt hay gradient trang trí.
6. **Bo tròn nhất quán (Radius 28px) & Đổ bóng mờ nhẹ nhàng**: Không dùng viền cứng, tạo cảm giác mềm mại, hiện đại và cao cấp.

---

## 2. Hệ thống Design Tokens

### 2.1. Bảng màu Trung tính — Neutral Palette (Chiếm ~95% giao diện)

| Token CSS | Tailwind Token | Mã Hex | Mục đích sử dụng |
|---|---|---|---|
| `--bg-page` | `bg-page` | `#F5F5F7` | Nền canvas tổng thể của trang web (chuyển nhẹ sang `#EDEDF0` ở chân trang) |
| `--bg-card` | `bg-white` | `#FFFFFF` | Nền các thẻ Card chức năng chính |
| `--bg-subtle` | `bg-subtle` | `#F4F4F6` | Vùng nền phụ bên trong card (khung preview, segmented tab, input background) |
| `--bg-subtle-hover` | `hover:bg-[#ECECEF]` | `#ECECEF` | Trạng thái hover của các nút phụ hoặc hàng trong bảng |
| `--border-hairline` | `border-hairline` | `#EFEFF2` | Đường kẻ chia mờ, dải phân cách nhẹ |
| `--border-card` | `border-card` | `#E9E9EE` | Viền ngoài mờ của Card (1px) |
| `--text-primary` | `text-primary` | `#0B0B0F` | Tiêu đề chính, con số lớn hero, giá trị then chốt |
| `--text-secondary` | `text-muted` | `#6B6B76` | Nhãn form, phụ đề, đơn vị tiền tệ, trạng thái phụ |
| `--text-tertiary` | `text-muted-soft` | `#9A9AA5` | Placeholder, timestamp, ghi chú giải thích mờ |
| `--ink` | `bg-ink text-white` | `#111114` | Nút hành động chính (Primary CTA "Xác nhận tạo quảng cáo") |

---

### 2.2. Bảng màu Dữ liệu & Trạng thái — Data & State Palette

Chỉ sử dụng cho trạng thái vận hành của Meta và thông số dữ liệu thật:

| Token CSS | Tailwind Token | Mã Hex | Mục đích & Ngữ nghĩa |
|---|---|---|---|
| `--data-1` | `data-1` | `#1F5FFF` | Nút "Connect Facebook", liên kết điều hướng, điểm nhấn dữ liệu chính |
| `--data-2` | `data-2` | `#B13BF0` | Tùy chọn thứ cấp / số liệu phụ |
| `--data-3` | `data-3` | `#FF8A1F` | Trạng thái cảnh báo, huy hiệu `PAUSED`, cảnh báo ngân sách |
| `--data-4` | `data-4` | `#1FA63A` | Trạng thái thành công, huy hiệu `Connected`, chỉ số tăng trưởng |
| `--data-alert` | `data-alert` | `#E5483D` | Lỗi Meta API, thông báo thất bại, trường nhập sai định dạng |

---

### 2.3. Hệ thống Bo góc — Corner Radius Scale

| Token CSS | Giá trị | Dùng cho |
|---|---|---|
| `--radius-xs` | `4px` | Bo góc thanh tiến trình, thẻ tag nhỏ |
| `--radius-sm` | `8px` | Tooltip, badge trạng thái nhỏ, ô input nhỏ |
| `--radius-md` | `12px` | Nút phụ full-width, khung ảnh xem trước, vùng subtle |
| `--radius-lg` | `16px` | Khung điều hướng phân tab (Segmented control) |
| `--radius-xl` | `28px` | **Toàn bộ các thẻ Card chính** |
| `--radius-full` | `999px` | Nút tròn icon, pill trạng thái kết nối |

---

### 2.4. Hệ thống Đổ bóng — Elevation & Shadow Scale

```css
/* Đổ bóng rộng và mờ tự nhiên cho Card */
--shadow-card: 0 1px 2px rgba(16, 16, 24, 0.04), 0 8px 24px rgba(16, 16, 24, 0.06);

/* Đổ bóng nhẹ cho nút điều khiển nhỏ, tab active */
--shadow-control: 0 1px 2px rgba(16, 16, 24, 0.08), 0 0 0 1px rgba(16, 16, 24, 0.04);

/* Đổ bóng cho nút bấm chính màu đen ink */
--shadow-primary: 0 6px 16px rgba(16, 16, 24, 0.22);
```

---

### 2.5. Hệ thống Chữ viết — Typography Scale

- **Phông chữ chủ đạo**: `Inter`, `Geist`, `-apple-system`, `Segoe UI`, `sans-serif`.
- **Cấu hình số**: Bắt buộc `font-feature-settings: "tnum" 1, "cv11" 1` (tabular numbers) để các con số căn thẳng cột trong bảng và số liệu tiền tệ.

| Cấp bậc (Role) | Size / Line-height | Weight | Màu mặc định | Ví dụ áp dụng |
|---|---|:---:|---|---|
| **Display** | 64px / 1.0 | 400 | `--text-primary` | Số lượng chiến dịch hero (`12`), số tiền (`50K`) |
| **Title Lg** | 28px / 1.15 | 500 | `--text-primary` | Tiêu đề card ("Tạo quảng cáo sản phẩm", "Chiến dịch") |
| **Title Md** | 18px / 1.25 | 600 | `--text-primary` | Tiêu đề phần, tên chiến dịch |
| **Value** | 15px / 1.3 | 500 | `--text-primary` | Giá trị dữ liệu trong bảng, ID tài nguyên |
| **Body** | 14px / 1.4 | 400 | `--text-primary` | Nội dung bài quảng cáo, văn bản hướng dẫn |
| **Label** | 13px / 1.3 | 400 | `--text-secondary` | Nhãn form ("Tài khoản quảng cáo", "Ngân sách ngày") |
| **Caption** | 12px / 1.3 | 400 | `--text-tertiary` | Thời gian tạo, chú thích an toàn `PAUSED` |

---

## 3. Quy chuẩn Tailwind CSS (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        page: '#F5F5F7',
        subtle: '#F4F4F6',
        ink: '#111114',
        border: {
          hairline: '#EFEFF2',
          card: '#E9E9EE',
        },
        primary: '#0B0B0F',
        muted: {
          DEFAULT: '#6B6B76',
          soft: '#9A9AA5',
        },
        data: {
          1: '#1F5FFF',
          2: '#B13BF0',
          3: '#FF8A1F',
          4: '#1FA63A',
          alert: '#E5483D',
        },
      },
      borderRadius: {
        card: '28px',
      },
      boxShadow: {
        card: '0 1px 2px rgba(16, 16, 24, 0.04), 0 8px 24px rgba(16, 16, 24, 0.06)',
        control: '0 1px 2px rgba(16, 16, 24, 0.08), 0 0 0 1px rgba(16, 16, 24, 0.04)',
        primary: '0 6px 16px rgba(16, 16, 24, 0.22)',
      },
      fontFamily: {
        sans: ['Inter', 'Geist', '-apple-system', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```
