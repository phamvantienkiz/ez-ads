# Brand Refactoring Plan: BAHA Ads Manager -> EZ-Ads

## 1. Mục tiêu
Chuyển đổi toàn bộ nhận diện thương hiệu từ **BAHA Ads Manager** (dự án demo tuyển dụng ban đầu) sang **EZ-Ads** (sản phẩm mã nguồn mở, portfolio cá nhân phục vụ demo cho nhiều bên đối tác/nhà tuyển dụng).

## 2. Chuẩn hóa tên thương hiệu (Brand Naming Convention)
- **Tên hiển thị thương hiệu chính thức**: `EZ-Ads` (hoặc `EZ-Ads Manager`)
  - Viết chuẩn: `EZ-Ads` (chữ "EZ" viết hoa để thể hiện cách phát âm "Easy", dấu gạch ngang phân tách thanh thoát, và "Ads" viết hoa chữ A theo danh từ chuẩn Title Case).
- **Slug / Package Identifier**: `ez-ads-manager-frontend`
- **Tên nhãn / Tiêu đề ứng dụng**: `EZ-Ads Manager — Meta Marketing Automation`
- **Domain ví dụ / URL**: `https://ezads.io` hoặc `https://ezads.vn`
- **LocalStorage key**: `ezads_meta_app_id` (với fallback kiểm tra `baha_meta_app_id` nếu có phiên cũ).
- **Fanpage / Campaign ví dụ**: `EZ Store` / `EZ-Ads Traffic Demo Campaign`

## 3. Phạm vi tệp cần refactor
1. **Frontend**:
   - `frontend/package.json`: Tên package.
   - `frontend/src/app/layout.tsx`: Title & description trang.
   - `frontend/src/app/page.tsx`: Dữ liệu mẫu (campaign, ad headline, primary text, placeholder, footer text, localStorage).
   - `frontend/src/components/Header.tsx`: Logo/Brand text trên header navbar.
   - `frontend/src/components/ConnectCard.tsx`: Hướng dẫn App ID, localStorage key.
   - `frontend/src/components/AdForm.tsx`: Placeholder và gợi ý mẫu.
   - `frontend/src/components/AdPreviewCard.tsx`: Preview domain fallback (`ezads.io` / `ezads.vn`).
   - `frontend/src/types/index.ts`: Comments và ví dụ TypeScript type.
2. **README Documentation**:
   - `README.md` (Bản tiếng Anh)
   - `README.vi.md` (Bản tiếng Việt)
3. **Showcase HTML (nếu cần hiển thị trực quan)**:
   - `docs/views/mvp-showcase.html`

## 4. Nguyên tắc thực hiện
- Không chạm vào backend logic/code/API.
- Dùng trực tiếp read_file và edit_file, tuyệt đối không dùng script python để sửa file.
- Đảm bảo build frontend chạy mượt mà, không lỗi lint/TypeScript.
