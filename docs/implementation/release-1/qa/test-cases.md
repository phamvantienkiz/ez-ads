# QA Test Plan & Test Cases — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Tài liệu tham chiếu**: [BAHA_Ads_Manager_MVP_Requirements.md](../../../requirement/BAHA_Ads_Manager_MVP_Requirements.md), [prd.md](../prd.md), [story-index.md](../backlog/story-index.md)  
**Ngày cập nhật**: 2026-10-17  
**Trạng thái**: Approved  

---

## 1. Phạm vi & Nguyên tắc Kiểm thử (Test Strategy)

- **Nguyên tắc cốt lõi**: Kiểm chứng luồng tích hợp thật 100% với **Meta Graph & Marketing API (`v20.0`)**. Tuyệt đối không dùng dữ liệu giả lập (mock) để đánh dấu hoàn thành các ca kiểm thử tích hợp.
- **An toàn tài chính**: Mọi ca kiểm thử tạo tài nguyên trên Meta bắt buộc phải xác minh trường `status = "PAUSED"` để ngăn chặn phát sinh chi phí quảng cáo thực tế.
- **Bảo mật**: Xác minh không rò rỉ `META_APP_SECRET`, `access_token`, hoặc `code` trên giao diện trình duyệt, DevTools Network response và console log.

---

## 2. Kịch bản Kiểm thử Chức năng Chính (Core Functional Test Cases)

| Mã TC | Liên kết Story / FR | Tên kịch bản kiểm thử | Điều kiện tiên quyết (Pre-conditions) | Các bước thực hiện (Test Steps) | Kết quả mong đợi (Expected Result) |
|---|---|---|---|---|---|
| **TC-01** | [US-001](../backlog/stories/US-001.md) (`FR-01`) | Kết nối Facebook qua OAuth thành công & lưu phiên | Đã cấu hình `.env` hợp lệ; chưa có bản ghi trong `meta_sessions`. | 1. Mở `http://localhost:3000`<br/>2. Nhấn nút `Connect Facebook`<br/>3. Đồng ý cấp quyền trên Meta | Backend xác minh `state`, đổi `code` lấy token, lưu vào `meta_sessions (id=1)`. UI hiển thị huy hiệu `Đã kết nối Meta`. |
| **TC-02** | [US-001](../backlog/stories/US-001.md) (`D-05`) | Duy trì phiên kết nối khi F5 trình duyệt hoặc restart backend | Đã đăng nhập thành công ở `TC-01`. | 1. Nhấn F5 trên trình duyệt<br/>2. Khởi động lại tiến trình Uvicorn rồi F5 lại | API `GET /api/meta/status` trả về `connected: true`. Người dùng không phải đăng nhập lại. |
| **TC-03** | [US-002](../backlog/stories/US-002.md) (`FR-02`) | Tải và chọn Ad Account thật từ Meta API | Đã kết nối Meta; tài khoản có ít nhất 1 Ad Account hợp lệ. | 1. Quan sát dropdown `Ad Account`<br/>2. Chọn 1 tài khoản quảng cáo | Hiển thị đúng Tên, ID (`act_...`) và `currency` (`VND`/`USD`) thật từ Meta. |
| **TC-04** | [US-003](../backlog/stories/US-003.md) (`FR-03`) | Tải và chọn Facebook Page đại diện | Đã kết nối Meta; tài khoản quản lý ít nhất 1 Fanpage. | 1. Mở dropdown `Facebook Page`<br/>2. Chọn 1 Fanpage | Hiển thị đúng Tên Page và Page ID thật từ `/me/accounts`. |
| **TC-05** | [US-004](../backlog/stories/US-004.md) (`FR-04`, `D-06`) | Kiểm tra quy đổi ngân sách tự động theo đơn vị tiền tệ | Chọn Ad Account có `currency = VND` hoặc `USD`. | 1. Nhập ngân sách `50000` (nếu VND) hoặc `20` (nếu USD)<br/>2. Kiểm tra payload gửi lên Meta | Với VND: gửi `"50000"`. Với USD: tự động nhân 100 thành `"2000"`. |
| **TC-06** | [US-005](../backlog/stories/US-005.md) (`FR-05`) | Xem trước trực quan (Live Preview) & Xác nhận an toàn | Đã điền đủ thông tin vào biểu mẫu quảng cáo. | 1. Quan sát thẻ `AdPreviewCard` bên cột phải<br/>2. Kiểm tra hộp cảnh báo `PAUSED` | Thẻ Preview hiển thị đúng Page, Primary Text, Ảnh, Headline, Domain, CTA `Tìm hiểu thêm` và cảnh báo trạng thái `PAUSED`. |
| **TC-07** | [US-006](../backlog/stories/US-006.md) (`FR-06`) | Thực thi chuỗi 5 bước tạo quảng cáo thật trên Meta API | Đã chọn Ad Account, Page và xác nhận tạo quảng cáo. | 1. Nhấn nút `Xác nhận tạo quảng cáo trên Meta`<br/>2. Chờ phản hồi từ backend | Tạo thành công tuần tự: `image_hash` $\rightarrow$ `campaign_id` $\rightarrow$ `adset_id` $\rightarrow$ `creative_id` $\rightarrow$ `ad_id` (tất cả ở trạng thái `PAUSED`). Lưu vào `ad_creation_runs`. |
| **TC-08** | [US-007](../backlog/stories/US-007.md) (`FR-07`) | Truy vấn danh sách chiến dịch thật & Làm mới (Refresh) | Đã tạo ít nhất 1 chiến dịch trên Ad Account. | 1. Chuyển sang tab `Campaigns`<br/>2. Nhấn nút `Refresh` | Bảng hiển thị danh sách chiến dịch thật từ Meta gồm Tên, ID, Objective (`OUTCOME_TRAFFIC`), Status (`PAUSED`), Thời gian tạo. |
| **TC-09** | [US-008](../backlog/stories/US-008.md) (`FR-08`, `FR-09`) | Kiểm tra Dashboard vận hành & Health Check | Backend và Frontend đang chạy. | 1. Mở tab `Dashboard`<br/>2. Kiểm tra `GET /api/health` | Hiển thị trạng thái kết nối, tài sản đang chọn, tổng số chiến dịch, và 4 ID thật của phiên chạy gần nhất. |

---

## 3. Ma trận Kiểm thử 12 Rủi ro & Trường hợp Lỗi Trọng yếu (Mục 11 Requirement)

| # | Trường hợp lỗi / Rủi ro trọng yếu | Mã TC | Cách thức mô phỏng (Test Trigger) | Phản hồi hệ thống bắt buộc (Expected Handling) |
|---|---|---|---|---|
| **1** | Meta App ID/Secret hoặc Redirect URI chưa cấu hình | **TC-E01** | Để trống `META_APP_ID` hoặc `META_APP_SECRET` trong `.env` rồi gọi `/api/meta/connect`. | Không crash server; trả về lỗi cấu hình rõ ràng hướng dẫn kiểm tra tệp `.env`. |
| **2** | OAuth bị người dùng hủy hoặc callback sai `state` | **TC-E02** | Nhấn Cancel trên Facebook hoặc sửa tham số `state` trên URL callback. | Chặn request (HTTP 400 `OAUTH_CSRF_MISMATCH` hoặc báo `OAUTH_ACCESS_DENIED`), cho phép thử lại. |
| **3** | Token hết hạn hoặc thiếu quyền (Permissions) | **TC-E03** | Thay token trong DB bằng chuỗi hết hạn hoặc thu hồi quyền trên Facebook. | Báo lỗi `TOKEN_EXPIRED` (401), hướng dẫn người dùng nhấn kết nối lại. |
| **4** | Không có Ad Account hoặc Facebook Page phù hợp | **TC-E04** | Đăng nhập bằng tài khoản Facebook trắng chưa có Ad Account / Fanpage. | Hiển thị Empty State kèm giải thích nguyên nhân thiếu quyền/tài sản; khóa nút tạo quảng cáo. |
| **5** | Ad Account không được phép quản lý quảng cáo | **TC-E05** | Gửi request tạo quảng cáo với `ad_account_id` không nằm trong danh sách quyền của user. | Backend từ chối trước khi tạo hoặc trả về thông báo thiếu quyền quản trị tài khoản. |
| **6** | Tài khoản quảng cáo bị hạn chế / thiếu phương thức thanh toán | **TC-E06** | Dùng Ad Account có `account_status != 1` hoặc chưa gắn thẻ thanh toán khi tạo Ad Set/Ad. | Hiển thị thông báo lỗi thực tế từ Meta (đã làm sạch token) giải thích tài khoản cần thiết lập thanh toán/đủ điều kiện. |
| **7** | Objective, targeting, budget, creative hoặc URL không hợp lệ | **TC-E07** | Nhập ngân sách âm/bằng 0, hoặc nhập `destinationUrl` sai định dạng `http(s)://`. | Chặn ngay tại tầng validation frontend & Pydantic (`422 VALIDATION_ERROR`), giữ nguyên dữ liệu đã nhập trên form. |
| **8** | Ảnh sản phẩm không truy cập được hoặc sai định dạng | **TC-E08** | Nhập `imageUrl` bị lỗi 404 hoặc không phải định dạng ảnh công khai. | Dừng ngay ở Bước 1 (`/adimages`), lưu trạng thái `failed`, báo lỗi `META_IMAGE_HASH_FAILED`. |
| **9** | Rate limit, timeout hoặc lỗi máy chủ Meta API | **TC-E09** | Ngắt mạng hoặc giả lập độ trễ $> 30\text{s}$ khi gọi Meta Graph API. | Bắt `httpx.TimeoutException`, trả về `504 META_API_TIMEOUT`, hiển thị thông báo an toàn. |
| **10** | **Partial Failure**: Campaign/Ad Set thành công nhưng Creative/Ad lỗi | **TC-E10** | Dùng dữ liệu hợp lệ cho Campaign/Ad Set nhưng truyền URL đích bị Meta từ chối ở bước Creative. | Lưu `status = 'partial_failure'` vào `ad_creation_runs`. UI hiển thị rõ `campaign_id`, `adset_id` đã tạo và báo lỗi ở bước `create_creative`. **Không báo thành công toàn bộ.** |
| **11** | Request timeout sau khi Meta đã tạo một phần tài nguyên | **TC-E11** | Timeout xảy ra ở bước 3 hoặc bước 4 sau khi bước 2 đã tạo Campaign. | **Tuyệt đối không tự động retry** lệnh tạo để tránh nhân đôi chiến dịch; hiển thị các ID đã ghi nhận được và yêu cầu kiểm tra danh sách chiến dịch. |
| **12** | Người dùng bấm nút Submit nhiều lần liên tiếp (Double-submit) | **TC-E12** | Nhấn đúp liên tục vào nút `Xác nhận tạo quảng cáo trên Meta`. | Nút submit bị vô hiệu hóa ngay lập tức (`isSubmitting = true`) và backend chặn bằng khóa chống gửi trùng (`409 DOUBLE_SUBMIT_LOCKED`). |

---

## 4. Checklist Nghiệm thu Trước và Trong Buổi Demo (Mục 13 & 17 Requirement)

### 4.1. Checklist Kỹ thuật & Tích hợp
- [ ] Frontend Next.js khởi chạy không lỗi tại `http://localhost:3000`.
- [ ] Backend FastAPI khởi chạy trong `.venv` tại `http://localhost:8000` và `/api/health` trả về `200 OK`.
- [ ] Luồng OAuth khởi tạo có `state` và xử lý callback thành công, lưu phiên vào SQLite `meta_sessions`.
- [ ] Tải được danh sách Ad Account thật và Facebook Page thật từ tài khoản BAHA cung cấp.
- [ ] Form tạo quảng cáo hoạt động mượt, có Live Preview và hộp cảnh báo trạng thái `PAUSED`.
- [ ] Gửi request thật tới Meta Marketing API `v20.0` và hiển thị trung thực các ID (`campaign_id`, `adset_id`, `creative_id`, `ad_id`) hoặc mã lỗi thực tế.
- [ ] Tab `Campaigns` tải được danh sách chiến dịch từ Meta API và có nút Refresh hoạt động.
- [ ] Kiểm tra toàn bộ response JSON và terminal logs: **0% rò rỉ `META_APP_SECRET` hoặc `access_token`**.

### 4.2. Checklist Vận hành Ngay Trước Giờ Trình Bày
- [ ] Đã kiểm tra tệp `.env` khớp chính xác `META_REDIRECT_URI=http://localhost:8000/api/meta/callback` trên Meta Developer Portal.
- [ ] Đã đăng nhập sẵn bằng đúng tài khoản Facebook có quyền Admin/Tester/Advertiser do BAHA cung cấp.
- [ ] Đã chuẩn bị sẵn bộ dữ liệu demo hợp lệ (Tên chiến dịch, URL sản phẩm HTTPS, URL ảnh công khai truy cập tốt, ngân sách phù hợp đơn vị tiền tệ).
- [ ] Xác nhận trạng thái tạo mặc định là `PAUSED` để không phát sinh chi tiêu ngoài ý muốn.
- [ ] Nhấn nút tạo 1 lần duy nhất, đối chiếu ID trả về trên ứng dụng với danh sách chiến dịch thực tế.
