# Bài Học Kinh Nghiệm Kết Nối Meta / Facebook Marketing API (Release 1 Demo)

> **Tài liệu:** Lessons Learned — Meta OAuth 2.0 & Marketing API Integration  
> **Dự án:** BAHA Ads Manager (MVP Release 1)  
> **Ngày cập nhật:** 17/10/2026  
> **Phạm vi:** Đúc kết thực tế từ quá trình tích hợp và demo kết nối tài khoản Meta/Facebook cấp sẵn (BAHA) với hệ thống Backend (`FastAPI`) + Frontend (`Next.js`).

---

## 1. Bối cảnh thực tế khi triển khai Demo

Trong quá trình chạy thử nghiệm kết nối thực tế với tài khoản Facebook Developer của khách hàng/đối tác (BAHA) trên trình duyệt đã đăng nhập sẵn phiên làm việc:

1. **Vấn đề 1 — Lỗi `"ID ứng dụng không hợp lệ"` (`Invalid App ID`):**
   - Khi bấm **"Connect Facebook ngay"**, nếu file [`backend/.env`](file:///E:/MyProject/BAHA/backend/.env) vẫn giữ giá trị mẫu (`META_APP_ID=test_meta_app_id`), Facebook OAuth Dialog (`https://www.facebook.com/v20.0/dialog/oauth`) sẽ từ chối ngay lập tức vì `client_id` phải là chuỗi số định danh ứng dụng thật trên `developers.facebook.com/apps/`.
2. **Vấn đề 2 — Rào cản bảo mật khi lấy `META_APP_SECRET` trên tài khoản khách hàng:**
   - Dù đã có quyền truy cập vào trình duyệt đang đăng nhập sẵn tài khoản Facebook của BAHA và xem được `META_APP_ID` công khai, việc nhấn nút **"Hiển thị" (Show)** để lấy `App Secret` trong mục *App Settings > Basic* **luôn buộc nhập lại mật khẩu tài khoản Facebook**.
   - Trong môi trường làm việc thực tế với khách hàng doanh nghiệp, khách hàng thường chỉ cấp phiên trình duyệt (hoặc quyền Developer/Tester) chứ **không chia sẻ mật khẩu cá nhân**. Do đó, luồng OAuth truyền thống (`Authorization Code Flow` cần cả `App ID` + `App Secret` ở phía Server) sẽ bị chặn nếu không có phương án thay thế.

---

## 2. Ba phương án kết nối Meta API và bài học lựa chọn

| Phương án | Cơ chế hoạt động | Yêu cầu thông tin | Ưu điểm | Hạn chế & Rủi ro | Khi nào nên dùng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Authorization Code Flow (Chuẩn Production)** | `response_type=code` -> Backend gọi `/oauth/access_token` kèm `client_secret` để đổi lấy User Token. | `META_APP_ID` + `META_APP_SECRET` + cấu hình `Valid OAuth Redirect URIs`. | Bảo mật cao nhất, token không bao giờ đi qua URL trình duyệt, dễ đổi sang Long-Lived Token (60 ngày). | Bắt buộc phải có `META_APP_SECRET` (cần mật khẩu Facebook để mở khóa). | Khi triển khai Production hoặc đội ngũ kỹ thuật tự sở hữu hoàn toàn Meta App. |
| **2. OAuth Implicit Flow (Cầu nối Hash Fragment)** | `response_type=token` -> Facebook trả trực tiếp `#access_token=...` trên thanh địa chỉ callback mà không cần `client_secret`. | Chỉ cần `META_APP_ID` + cấu hình `Valid OAuth Redirect URIs`. | Không cần mật khẩu để xem `App Secret`; trải nghiệm bấm nút **"Connect Facebook"** mượt mà trên UI. | Cần bật *Client OAuth Login* trong sản phẩm *Facebook Login* của Meta App và khai báo đúng URI callback. | Khi có `App ID` và cấu hình được Redirect URI nhưng không có `App Secret`. |
| **3. Direct Token Injection qua Graph API Explorer (Thực tế nhanh nhất cho Demo)** | Lấy `Access Token` (`EAAB...`) từ `developers.facebook.com/tools/explorer/` gắn với `Meta App ID` và nạp vào phiên SQLite của hệ thống. | Chỉ cần phiên đăng nhập trên trình duyệt + chọn đúng App trên Graph API Explorer. | **Nhanh và chắc chắn nhất cho buổi Demo (100% thành công)**; bỏ qua mọi rào cản về mật khẩu `App Secret` lẫn cấu hình `Redirect URI`. | Token ngắn hạn (thường hết hạn sau 1–2 giờ), thao tác copy/paste thủ công lần đầu. | **Khuyên dùng số 1 khi chạy Live Demo gấp** trên máy/tài khoản của khách hàng. |

---

## 3. Các bài học kỹ thuật quan trọng (Key Technical Takeaways)

### Bài học 1: Luôn thiết kế "Dual-Mode Authentication" cho các bản MVP / Demo
Khi tích hợp với các nền tảng OAuth khắt khe như Meta/Facebook trong thời gian ngắn (2 giờ):
- Không nên khóa cứng hệ thống vào duy nhất một luồng `Authorization Code Flow` phụ thuộc hoàn toàn vào file `.env` tĩnh.
- **Giải pháp đã áp dụng trong dự án:**
  - Tại [`MetaAuthService`](file:///E:/MyProject/BAHA/backend/app/services/meta_auth_service.py): Hỗ trợ tự động chuyển đổi giữa `response_type=code` (khi có `META_APP_SECRET`) và `response_type=token` (khi chỉ có `META_APP_ID`), đồng thời cho phép truyền `app_id` động từ giao diện.
  - Tại [`meta_auth.py`](file:///E:/MyProject/BAHA/backend/app/api/v1/endpoints/meta_auth.py): Bổ sung endpoint `POST /api/v1/meta/token-callback` và cầu nối `IMPLICIT_OAUTH_BRIDGE_HTML` để vừa bắt được `#access_token` từ URL hash, vừa cho phép nạp trực tiếp token từ **Graph API Explorer** trên [`ConnectCard.tsx`](file:///E:/MyProject/BAHA/frontend/src/components/ConnectCard.tsx).

### Bài học 2: Hiểu rõ cơ chế URL Hash Fragment (`#access_token`) của trình duyệt
- Khi dùng `response_type=token`, Facebook redirect về:
  ```text
  http://localhost:8000/api/meta/callback#access_token=EAAB...&state=baha_...
  ```
- **Lưu ý quan trọng:** Trình duyệt web **không bao giờ** gửi phần sau dấu `#` (hash fragment) lên HTTP Server trong gói tin `GET`.
- Do đó, endpoint [`GET /api/v1/meta/callback`](file:///E:/MyProject/BAHA/backend/app/api/v1/endpoints/meta_auth.py#L84-L115) nếu không thấy query param `?code=` sẽ phải trả về một trang HTML chứa đoạn JavaScript nhỏ (`window.location.hash`) để đọc `access_token` tại trình duyệt rồi gửi `POST` về Backend lưu vào SQLite `meta_sessions`.

### Bài học 3: Phân quyền (Permissions / Scopes) trên Graph API Explorer
Khi lấy token qua `https://developers.facebook.com/tools/explorer/` để kết nối cho ứng dụng quản lý quảng cáo và Fanpage:
- **Quyền cơ bản để kết nối và đọc tài sản (Luôn hoạt động ngay):**
  - `public_profile`: Xác thực danh tính người dùng.
  - `ads_read`: Đọc danh sách tài khoản quảng cáo (`GET /me/adaccounts`) và danh sách chiến dịch (`GET /act_{id}/campaigns`).
  - `pages_show_list`, `pages_read_engagement`: Đọc danh sách Fanpage (`GET /me/accounts`).
- **Quyền khởi tạo quảng cáo & đăng bài (Cần cấp thêm trong hộp thoại Permissions của Explorer):**
  - `ads_management`: Bắt buộc nếu muốn thực thi pipeline 5 bước tạo Campaign / Ad Set / Creative / Ad.
  - `pages_manage_ads`, `pages_manage_posts`: Bắt buộc nếu muốn gắn Fanpage vào mẫu quảng cáo (`object_story_spec`) hoặc đăng bài viết trực tiếp lên Fanpage.

### Bài học 4: Rào cản ngoài code khi tạo Quảng cáo thật (Meta Ads) và Phương án Dự phòng (Fallback)
Trong thực tế, ngay cả khi kết nối OAuth/Token thành công 100% và code gọi đúng chuẩn Meta Marketing API v20.0, bước tạo quảng cáo vẫn có thể bị Meta chặn bởi **điều kiện tài khoản kinh doanh**:
1. **Tài khoản quảng cáo (`Ad Account`) chưa thêm thẻ thanh toán (Payment Method):** Meta thường chặn ở bước tạo `Ad Set` hoặc `Ad` với mã lỗi yêu cầu thiết lập phương thức thanh toán.
2. **Ứng dụng Meta App đang ở chế độ Development (Chưa chuyển sang Live):** Một số quyền nâng cao hoặc tài khoản quảng cáo không thuộc quyền sở hữu trực tiếp của Admin App sẽ bị giới hạn.
3. **Chiến lược Fallback an toàn khi Demo:**
   - Luôn tách biệt bước **Chứng minh kết nối & Đồng bộ tài sản thực tế** (`Connected` -> hiển thị đúng `Ad Account` và `Fanpage` từ Graph API) với bước **Ghi dữ liệu (Write API)**.
   - Trang bị sẵn luồng dự phòng [`POST /api/v1/ads/page-post`](file:///E:/MyProject/BAHA/backend/app/api/v1/endpoints/ads.py#L182-L233) (đăng bài trực tiếp lên Fanpage qua `/{page_id}/photos` hoặc `/{page_id}/feed`) để đề phòng trường hợp `Ad Account` chưa có thẻ thanh toán.

---

## 4. Quy trình chuẩn (SOP) để chạy Demo nhanh trong 2 phút

Khi cần tái현 (reproduce) buổi demo trên bất kỳ máy tính hoặc tài khoản Facebook nào khác mà không có mật khẩu:

1. **Bước 1:** Mở trình duyệt đã đăng nhập Facebook, truy cập `https://developers.facebook.com/apps/` để copy **App ID** (dãy số).
2. **Bước 2:** Mở `https://developers.facebook.com/tools/explorer/`:
   - Chọn đúng ứng dụng tại ô **Meta App**.
   - Tại ô **Permissions**, chọn thêm: `ads_read`, `ads_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads`.
   - Nhấn **Generate Access Token** và xác nhận cấp quyền trên cửa sổ bật lên (không cần mật khẩu).
   - Copy chuỗi **Access Token (`EAAB...`)**.
3. **Bước 3:** Mở giao diện BAHA Ads Manager (`http://localhost:3000`):
   - Điền **Meta App ID** vào ô nhập trên thẻ kết nối.
   - Bấm **"Hoặc dán trực tiếp Access Token"** -> Dán chuỗi `EAAB...` -> Nhấn **"Lưu Token & Kết nối"**.
4. **Bước 4:** Hệ thống chuyển sang trạng thái **Connected**, lưu phiên an toàn vào SQLite (`meta_sessions`) và tự động nạp danh sách **Ad Accounts**, **Fanpage** cùng **Campaigns** thực tế lên Dashboard.
