# BAHA Ads Manager — MVP Requirements

> **Mục tiêu:** Hoàn thành một web app full-stack có thể demo trong khoảng **2 giờ**, dùng để kết nối Meta/Facebook, chọn tài khoản quảng cáo và Fanpage, tạo quảng cáo sản phẩm qua **Meta Marketing API chính thức**, rồi hiển thị kết quả thực tế.
>
> **Ưu tiên tuyệt đối:** Một luồng demo end-to-end chạy được. Không xây sản phẩm hoàn chỉnh, không làm tính năng phụ, không giả lập kết quả API thật.

---

## 1. Bối cảnh và mục tiêu

BAHA cần một ứng dụng web nội bộ để hỗ trợ thao tác quảng cáo sản phẩm trên Facebook. Người demo sẽ dùng tài khoản Facebook và quyền truy cập do BAHA cung cấp.

Ứng dụng cần cho phép người dùng:
1. Kết nối với Facebook bằng OAuth.
2. Xem và chọn một tài khoản quảng cáo Meta mà tài khoản Facebook được cấp quyền truy cập.
3. Chọn một Facebook Page có thể dùng để chạy quảng cáo.
4. Nhập nội dung quảng cáo sản phẩm, URL đích và thông tin ngân sách cơ bản.
5. Xem lại nội dung và xác nhận trước khi gửi yêu cầu tạo quảng cáo.
6. Tạo tài nguyên quảng cáo qua Meta Marketing API.
7. Hiển thị ID và trạng thái thực tế mà Meta trả về, cùng danh sách chiến dịch đã tạo nếu API cho phép truy vấn.

**Định nghĩa thành công của demo:** Ứng dụng gửi được yêu cầu tạo quảng cáo tới Meta API và hiển thị kết quả thật. Việc tạo thành công tài nguyên quảng cáo không đồng nghĩa quảng cáo đã được Meta duyệt hoặc đã bắt đầu phân phối.

## 2. Phạm vi MVP

### 2.1 Bắt buộc — P0

- Giao diện web chạy được trên máy demo.
- Backend FastAPI hoạt động và gọi Meta API từ server.
- OAuth kết nối tài khoản Facebook, với callback URL được cấu hình.
- Lấy danh sách ad account mà người dùng hiện tại có quyền truy cập.
- Lấy danh sách Facebook Page phù hợp với quyền truy cập.
- Form tạo quảng cáo sản phẩm tối thiểu.
- Gửi yêu cầu tạo các tài nguyên cần thiết bằng Meta Marketing API.
- Hiển thị kết quả thật: thành công/thất bại, mã lỗi, resource IDs và trạng thái trả về.
- Hiển thị các chiến dịch đã tạo hoặc một trạng thái rỗng có giải thích.
- README hướng dẫn chạy và cấu hình môi trường.

### 2.2 Không làm trong 2 giờ — ngoài phạm vi

- Hệ thống người dùng/đăng nhập nội bộ riêng.
- Phân quyền nhiều vai trò, tổ chức hoặc nhiều khách hàng.
- Thanh toán, hóa đơn, quản lý chi phí nâng cao.
- Dashboard phân tích chuyên sâu, biểu đồ nhiều bộ lọc.
- AI viết nội dung quảng cáo, A/B testing, tự động tối ưu chiến dịch.
- Lập lịch đăng quảng cáo, quy trình phê duyệt nhiều cấp.
- Upload thư viện media, quản lý asset phức tạp.
- Tạo tài khoản quảng cáo mới qua ứng dụng.
- Tự động xử lý mọi trường hợp lỗi của Meta.
- Dữ liệu mẫu giả làm dữ liệu thật.

Có thể dùng dữ liệu tĩnh chỉ cho các yếu tố giao diện không mang tính nghiệp vụ, nhưng mọi tài khoản, chiến dịch, ID, trạng thái và thông báo thành công liên quan đến Meta phải lấy từ API thật hoặc được ghi rõ là dữ liệu demo.

## 3. Tech stack bắt buộc

- **Frontend:** Next.js + TypeScript + Tailwind CSS.
- **Backend:** Python + FastAPI.
- **Database:** SQLite.
- **External API:** Meta Graph API / Marketing API.
- **Integration:** OAuth của Meta/Facebook.
- **HTTP client backend:** thư viện Python phù hợp như `httpx`.
- **ORM/migration:** chỉ thêm nếu cần; ưu tiên đơn giản trong giới hạn thời gian.
- **Run mode:** local development phục vụ demo.

Không bổ sung Docker, Redis, queue, microservices hay hạ tầng triển khai production trừ khi repo hiện tại đã có sẵn và dùng được ngay.

## 4. Người dùng và giả định

### 4.1 Người dùng chính

Một người đại diện BAHA thao tác trực tiếp trên ứng dụng trong buổi demo.

### 4.2 Giả định cần kiểm chứng sớm

- BAHA cung cấp tài khoản Facebook có quyền truy cập một ad account và một Facebook Page phù hợp.
- Có thể cấu hình Meta App ID, App Secret, OAuth redirect URI và quyền cần thiết.
- Meta app, tài khoản và quyền API đủ điều kiện thực hiện các thao tác Marketing API cần thiết.
- Môi trường demo có thể truy cập callback URL. Nếu dùng local, cần một URL callback hợp lệ mà Meta chấp nhận; có thể cần HTTPS/tunnel tùy cấu hình.
- Có sẵn URL website sản phẩm hợp lệ và ảnh sản phẩm có thể truy cập bằng URL công khai nếu luồng tạo creative yêu cầu ảnh.

**Không được mặc định** rằng đăng nhập Facebook thành công đồng nghĩa có quyền quản lý quảng cáo. Quyền, token, ad account, Page, trạng thái tài khoản, phương thức thanh toán và các giới hạn của Meta đều có thể chặn luồng demo.

## 5. Luồng demo chính

1. Người dùng mở ứng dụng.
2. Ứng dụng hiển thị trạng thái kết nối Meta: chưa kết nối hoặc đã kết nối.
3. Người dùng nhấn **Connect Facebook**.
4. Backend tạo URL OAuth có `state`; frontend chuyển hướng người dùng sang Meta.
5. Meta chuyển về callback; backend xác minh `state`, xử lý authorization code và lấy token ở server.
6. Backend lấy danh sách ad account có thể truy cập.
7. Người dùng chọn ad account.
8. Backend lấy danh sách Page có thể sử dụng; người dùng chọn Page.
9. Người dùng điền thông tin quảng cáo sản phẩm.
10. Ứng dụng hiển thị bản xem trước nội dung và tóm tắt ngân sách/đối tượng/cấu hình.
11. Người dùng nhấn **Create Ad** và xác nhận thao tác.
12. Backend gọi Meta Marketing API để tạo các tài nguyên cần thiết theo đúng thứ tự.
13. Ứng dụng hiển thị kết quả thực tế từ Meta: resource IDs, trạng thái, lỗi nếu có.
14. Người dùng có thể quay về danh sách chiến dịch và tải lại dữ liệu từ Meta.

### Quy tắc an toàn khi demo

- **Mặc định tạo chiến dịch/tài nguyên ở trạng thái `PAUSED`** nếu quy trình API cho phép, sau đó hiển thị rõ trạng thái. Chỉ cho phép bật chạy nếu người dùng chủ động xác nhận và BAHA yêu cầu.
- Nếu bài test yêu cầu quảng cáo bắt đầu phân phối ngay, cần xác nhận trước khi chuyển trạng thái sang hoạt động và hiển thị cảnh báo rằng có thể phát sinh chi phí.
- Không tự động bật chiến dịch hoặc tăng ngân sách.
- Không tự retry thao tác tạo tài nguyên khi kết quả lần gọi trước chưa rõ; có nguy cơ tạo trùng. Hãy hiển thị lỗi và yêu cầu kiểm tra trước khi thử lại.
- Không tuyên bố quảng cáo đã được duyệt hoặc đang phân phối nếu API không xác nhận điều đó.

## 6. Functional requirements

### FR-01 — Kết nối Facebook

- Trang chính có nút **Connect Facebook**.
- OAuth được khởi tạo và xử lý ở backend.
- Dùng tham số `state` để chống CSRF và xác minh lại tại callback.
- Token được xử lý ở backend; không gửi App Secret hoặc token dài hạn cho frontend.
- Sau callback, hiển thị trạng thái kết nối rõ ràng.
- Nếu người dùng từ chối quyền, callback lỗi hoặc token không hợp lệ, hiển thị thông báo có thể hiểu được và cho phép thử lại.

**Acceptance criteria**
- [ ] Người dùng có thể bắt đầu OAuth từ ứng dụng.
- [ ] Callback thành công hoặc lỗi được xử lý rõ ràng.
- [ ] Không có App Secret/token nhạy cảm trong mã frontend hoặc log.
- [ ] Không hiển thị “Connected” nếu chưa xác minh được kết nối.

### FR-02 — Chọn tài khoản quảng cáo

- Lấy danh sách ad account thông qua Meta API bằng token hiện tại.
- Hiển thị tối thiểu tên và ID tài khoản; hiển thị currency nếu API trả về.
- Người dùng chọn một tài khoản trước khi tạo quảng cáo.
- Nếu danh sách rỗng, giải thích rằng tài khoản Facebook có thể chưa được cấp quyền hoặc quyền/token hiện tại chưa đủ.

**Acceptance criteria**
- [ ] Danh sách lấy từ API thật.
- [ ] Không hardcode ID tài khoản của BAHA.
- [ ] Backend xác minh account ID thuộc danh sách có thể truy cập trước khi tạo tài nguyên.

### FR-03 — Chọn Facebook Page

- Lấy danh sách Page mà người dùng/token có quyền truy cập.
- Hiển thị tên và ID Page.
- Người dùng chọn Page dùng làm danh tính quảng cáo.
- Nếu không có Page phù hợp, hiển thị lỗi và hướng dẫn kiểm tra quyền Page.

**Acceptance criteria**
- [ ] Danh sách Page lấy từ API thật.
- [ ] Backend kiểm tra Page được chọn trước khi tạo creative/ad.
- [ ] Không giả định mọi Facebook user đều có Page phù hợp.

### FR-04 — Form tạo quảng cáo sản phẩm

Form tối thiểu gồm:

| Trường | Bắt buộc | Ghi chú |
|---|---:|---|
| Ad account | Có | Chọn từ danh sách đã tải |
| Facebook Page | Có | Chọn từ danh sách đã tải |
| Campaign name | Có | Tên dễ nhận biết |
| Objective | Có | Chỉ hiển thị objective được luồng API MVP hỗ trợ |
| Budget type | Có | Daily hoặc lifetime nếu objective/API hỗ trợ |
| Budget amount | Có | Giá trị dương; xác nhận đơn vị tiền tệ |
| Ad set name | Có | Có thể gợi ý từ campaign name |
| Ad name | Có | Có thể gợi ý từ campaign name |
| Primary text | Có | Nội dung chính |
| Headline | Khuyến nghị | Tùy định dạng creative |
| Destination URL | Có | URL hợp lệ, dùng HTTPS nếu phù hợp |
| Image URL | Có nếu creative yêu cầu | URL ảnh công khai, truy cập được |
| CTA | Có nếu định dạng yêu cầu | Chọn trong các CTA được hỗ trợ |
| Status | Có | Mặc định `PAUSED` |

Không xây form audience targeting phức tạp trong MVP. Nếu API yêu cầu targeting, sử dụng cấu hình tối thiểu hợp lệ và có giải thích trong UI; không tự ý đặt targeting nhạy cảm hoặc giả định cấu hình nào phù hợp với mọi chiến dịch.

### FR-05 — Preview và xác nhận

Trước khi gọi API, hiển thị:
- Tên campaign, objective và ad account.
- Page được chọn.
- Nội dung chính, headline, ảnh và URL đích.
- Ngân sách, loại ngân sách và trạng thái ban đầu.
- Cảnh báo về chi phí nếu có thao tác bật phân phối.

Người dùng phải nhấn nút xác nhận rõ ràng để gửi yêu cầu tạo quảng cáo.

### FR-06 — Tạo quảng cáo bằng Meta Marketing API

Backend chịu trách nhiệm thực hiện các request. Không gọi Marketing API trực tiếp từ trình duyệt.

Triển khai đúng thứ tự tài nguyên mà objective/format được chọn yêu cầu. Luồng thông thường có thể bao gồm:
1. Campaign.
2. Ad Set với ngân sách, lịch chạy và targeting hợp lệ.
3. Ad Creative.
4. Ad.

Tên endpoint, trường bắt buộc, phiên bản API và yêu cầu quyền phải được kiểm tra theo tài liệu Meta hiện hành. Không đoán tên field hoặc giả định mọi objective dùng chung một payload.

- Sử dụng ad account đã được chọn và xác minh.
- Gửi status `PAUSED` theo mặc định nếu được hỗ trợ.
- Lưu ID và status trả về cho từng tài nguyên đã tạo.
- Nếu một bước thất bại sau khi các bước trước đã thành công, hiển thị tài nguyên nào đã được tạo và bước nào thất bại; không báo thành công toàn bộ.
- Trả thông báo lỗi Meta có chọn lọc, loại bỏ token/secret và dữ liệu nhạy cảm khỏi nội dung lỗi.
- Không giả lập thành công khi API lỗi hoặc chưa được cấu hình.

**Acceptance criteria**
- [ ] Có request thật tới Meta Marketing API.
- [ ] Có kết quả thật từ API, bao gồm ID hoặc lỗi cụ thể.
- [ ] UI phân biệt “tạo tài nguyên thành công”, “đang chờ duyệt”, “bị từ chối/lỗi” và “đang phân phối” nếu API cung cấp thông tin tương ứng.
- [ ] Không tuyên bố đã publish thành công chỉ dựa vào việc tạo một campaign.
- [ ] Không có token/secret trong response frontend hoặc log.

### FR-07 — Danh sách chiến dịch

- Có trang/khối **Campaigns** hiển thị chiến dịch từ ad account đang chọn.
- Hiển thị tối thiểu: tên, ID, objective nếu có, status và thời điểm tạo nếu API cung cấp.
- Có nút refresh để truy vấn dữ liệu mới.
- Nếu chưa có chiến dịch, hiển thị empty state.
- Nếu API không khả dụng, hiển thị lỗi riêng; không thay bằng dữ liệu giả mà không gắn nhãn.

### FR-08 — Dashboard tối giản

Dashboard ưu tiên trạng thái vận hành, không cần hệ thống analytics hoàn chỉnh.

Hiển thị:
- Meta connection status.
- Ad account đang chọn.
- Page đang chọn.
- Số chiến dịch tải được từ API.
- Danh sách chiến dịch gần đây.
- Kết quả tạo quảng cáo gần nhất.

Nếu có thể lấy Insights trong thời gian còn lại, bổ sung một vài chỉ số như spend, impressions, reach, clicks. **Không để Insights chặn luồng tạo quảng cáo**; nếu không triển khai kịp, ghi rõ “Insights chưa được bật trong MVP”.

### FR-09 — Trạng thái tải và lỗi

Các thao tác gọi API cần có:
- Loading state.
- Error state.
- Empty state.
- Nút thử lại chỉ cho các thao tác đọc an toàn.
- Vô hiệu hóa nút submit trong khi request tạo tài nguyên đang chạy.
- Thông báo lỗi dễ hiểu và giữ lại dữ liệu form khi có thể.

## 7. Non-functional requirements

### NFR-01 — Bảo mật tối thiểu

- App Secret chỉ tồn tại ở backend environment.
- Không commit `.env` hoặc credentials.
- Không trả token cho frontend.
- Không log access token, App Secret, authorization code hoặc toàn bộ callback URL chứa code.
- OAuth callback phải xác minh `state`.
- Chỉ cho phép redirect/callback URL đã cấu hình.
- Backend kiểm tra dữ liệu đầu vào, URL, ngân sách và ad account được chọn.
- Với demo một người dùng, SQLite có thể lưu trạng thái/tài nguyên cần thiết; nếu lưu token, giới hạn quyền truy cập file DB và bảo vệ dữ liệu nhạy cảm. Không lưu token nếu không cần thiết.
- Không thêm chức năng đăng nhập nội bộ nếu không cần cho demo và không có thời gian.

### NFR-02 — Tính trung thực của dữ liệu

- Dữ liệu Meta phải lấy từ API.
- ID, trạng thái và lỗi phải phản ánh response thực.
- Không tạo nút “Publish successfully” giả.
- Nếu chạy chế độ mock để phát triển UI, phải hiển thị rõ `DEMO/MOCK MODE` và không dùng mock làm bằng chứng hoàn thành yêu cầu tích hợp thật.

### NFR-03 — Khả năng chạy

- Có hướng dẫn khởi chạy frontend và backend.
- Cấu hình nằm trong environment variables.
- SQLite tự khởi tạo bảng theo cách đơn giản, dễ chạy.
- Lỗi thiếu cấu hình Meta được thông báo rõ thay vì khiến ứng dụng crash khó hiểu.

## 8. Backend API contract đề xuất

Các route dưới đây là hợp đồng nội bộ gợi ý; có thể điều chỉnh theo cấu trúc repo hiện có.

| Method | Route | Mục đích |
|---|---|---|
| GET | `/api/health` | Kiểm tra backend |
| GET | `/api/meta/connect` | Tạo/chuyển hướng sang OAuth |
| GET | `/api/meta/callback` | Xử lý OAuth callback |
| GET | `/api/meta/status` | Trạng thái kết nối |
| GET | `/api/meta/ad-accounts` | Lấy ad accounts có quyền truy cập |
| GET | `/api/meta/pages` | Lấy Pages có thể sử dụng |
| GET | `/api/campaigns?ad_account_id=...` | Lấy chiến dịch |
| POST | `/api/ads` | Tạo campaign/ad set/creative/ad |
| GET | `/api/ads/{id}` | Xem kết quả tạo nếu cần |
| GET | `/api/insights?ad_account_id=...` | Tùy chọn, chỉ triển khai nếu còn thời gian |

### Quy ước response

Response thành công nên có cấu trúc nhất quán, ví dụ:
- `success`: boolean.
- `data`: dữ liệu trả về.
- `message`: thông báo ngắn.

Response lỗi nên có:
- `success: false`.
- `error.code`: mã lỗi nội bộ.
- `error.message`: thông báo an toàn, có thể hiển thị.
- `error.details`: tùy chọn, đã loại bỏ thông tin bí mật.

Không trả raw exception hoặc token về frontend.

## 9. SQLite — dữ liệu tối thiểu

Không thiết kế schema quá mức. Chỉ tạo bảng nếu ứng dụng thực sự cần lưu dữ liệu qua lần tải lại.

### Bảng `ad_creation_runs` (đề xuất)

- `id`: primary key.
- `ad_account_id`: ID tài khoản Meta.
- `page_id`: ID Page.
- `campaign_id`: ID trả về từ Meta, nullable nếu bước campaign thất bại.
- `adset_id`: ID trả về từ Meta, nullable.
- `creative_id`: ID trả về từ Meta, nullable.
- `ad_id`: ID trả về từ Meta, nullable.
- `status`: `pending`, `success`, `partial_failure`, `failed`.
- `request_summary`: JSON/text không chứa token hoặc secret.
- `error_message`: thông báo đã làm sạch.
- `created_at`: timestamp.

Không cần lưu toàn bộ dữ liệu Meta trừ khi phục vụ trực tiếp cho demo. Nếu deadline quá gấp, có thể ưu tiên hoàn thiện luồng tạo quảng cáo và dùng SQLite cho log kết quả tối thiểu hoặc bỏ persistence không thiết yếu, nhưng phải nêu rõ trong README.

## 10. Cấu hình môi trường

Tạo `.env.example` với các biến phù hợp, tối thiểu:

```dotenv
META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=http://localhost:8000/api/meta/callback
META_API_VERSION=
FRONTEND_URL=http://localhost:3000
DATABASE_URL=sqlite:///./baha_ads_manager.db
```

- Kiểm tra callback URI có khớp chính xác cấu hình trong Meta App hay không.
- Phiên bản API phải được chọn từ tài liệu Meta hiện hành, không dùng giá trị bịa.
- Không commit `.env`.
- Nếu cần tunnel/HTTPS cho OAuth callback, ghi rõ cách cấu hình trong README.
- Không coi `.env.example` là nơi điền credentials thật.

## 11. Error handling và các rủi ro trọng yếu

Phải xử lý/hiển thị tối thiểu những trường hợp sau:

1. Meta App ID/Secret hoặc redirect URI chưa cấu hình.
2. OAuth bị hủy hoặc callback không hợp lệ.
3. Token hết hạn hoặc thiếu quyền.
4. Không có ad account hoặc Page phù hợp.
5. Ad account không được phép quản lý quảng cáo.
6. Tài khoản quảng cáo bị hạn chế, thiếu phương thức thanh toán hoặc không đủ điều kiện.
7. Objective, targeting, budget, creative hoặc URL không hợp lệ.
8. Ảnh không truy cập được hoặc không đúng yêu cầu.
9. Rate limit, timeout hoặc lỗi Meta API.
10. Campaign tạo thành công nhưng Ad Set/Creative/Ad thất bại.
11. Request timeout sau khi Meta đã tạo một phần tài nguyên.
12. Người dùng bấm submit nhiều lần.

**Quy tắc:** Không tự động lặp lại thao tác tạo tài nguyên sau timeout khi chưa xác minh kết quả. Nếu chỉ tạo được một phần, hiển thị chính xác ID tài nguyên đã tạo và bước thất bại.

## 12. Thiết kế giao diện tối thiểu

Một layout dashboard đơn giản, responsive, ưu tiên desktop.

### Trang chính

- Header: `BAHA Ads Manager`, trạng thái kết nối Meta, nút Connect/Disconnect nếu có.
- Khu vực account selector: ad account và Page.
- Navigation hoặc tabs: `Dashboard`, `Create Ad`, `Campaigns`.
- Dashboard: account/Page đang chọn, kết quả gần nhất, danh sách campaign.
- Create Ad: form theo mục FR-04, preview và nút xác nhận.
- Result panel: trạng thái, campaign/ad set/creative/ad IDs, thông báo lỗi hoặc thành công.

Không dành thời gian làm animation, design system phức tạp hoặc biểu đồ trang trí. Ưu tiên form dễ thao tác, trạng thái rõ và không gây nhầm lẫn.

## 13. Acceptance checklist — tiêu chí hoàn thành

### Luồng tích hợp
- [ ] Frontend Next.js chạy được.
- [ ] Backend FastAPI chạy được.
- [ ] Health check hoạt động.
- [ ] OAuth bắt đầu và callback được xử lý.
- [ ] Có thể tải danh sách ad account thật.
- [ ] Có thể tải danh sách Page thật.
- [ ] Có thể chọn ad account và Page.
- [ ] Có thể nhập thông tin quảng cáo và xem preview.
- [ ] Backend gửi request tạo tài nguyên qua Meta Marketing API thật.
- [ ] UI hiển thị IDs/status/error thật từ Meta.
- [ ] Danh sách campaign truy vấn từ Meta hoặc có lỗi/empty state trung thực.
- [ ] Không lộ credentials/token.

### Demo và tài liệu
- [ ] README có lệnh chạy FE/BE.
- [ ] README liệt kê Meta App configuration và permissions cần kiểm tra.
- [ ] Có checklist demo ngắn.
- [ ] Đã kiểm tra đường đi từ Connect Facebook đến kết quả tạo quảng cáo.
- [ ] Nếu không thể tạo quảng cáo thật do thiếu quyền/cấu hình, ghi rõ nguyên nhân; không giả vờ đã hoàn thành tích hợp.

## 14. Kế hoạch thực hiện 2 giờ

Đây là phân bổ thời gian có tính định hướng, không phải bảo đảm rằng Meta API sẽ hoạt động nếu quyền/tài khoản chưa sẵn sàng.

| Thời gian | Việc cần hoàn thành | Ưu tiên |
|---|---|---|
| 0–10 phút | Kiểm tra repo, môi trường, Meta credentials, callback, quyền và ad account/Page | Chặn sớm rủi ro tích hợp |
| 10–25 phút | Tạo skeleton FE/BE, `.env.example`, health check, README ngắn | P0 |
| 25–55 phút | OAuth, token handling, lấy ad accounts và Pages | P0 |
| 55–90 phút | Form quảng cáo + tạo tài nguyên Meta theo một objective/format duy nhất | P0 |
| 90–105 phút | Hiển thị kết quả thật, campaign list và error states | P0 |
| 105–115 phút | Chạy thử end-to-end, sửa lỗi blocker | P0 |
| 115–120 phút | Chuẩn bị demo, kiểm tra ngân sách/status và ghi chú giới hạn | P0 |

### Quy tắc cắt phạm vi

Nếu thời gian thiếu:
1. Chỉ hỗ trợ **một objective và một format quảng cáo** đã xác minh payload API.
2. Chỉ hỗ trợ một ad account, một Page và một luồng tạo quảng cáo.
3. Bỏ Insights/biểu đồ.
4. Bỏ chỉnh sửa campaign, pause/resume và các chức năng quản trị khác.
5. Không bỏ OAuth/API thật để thay bằng mock mà vẫn tuyên bố hoàn thành.

Nếu OAuth hoặc quyền Meta chưa hoạt động trong 10–15 phút đầu, hãy xác định nguyên nhân ngay. Đây có thể là blocker từ cấu hình tài khoản/app chứ không phải lỗi code; cần ghi lại bằng chứng lỗi và tiếp tục phát triển phần còn lại mà không trình bày mock như một tích hợp thật.

## 15. Hướng dẫn làm việc với Antigravity

Yêu cầu Antigravity thực hiện theo từng phase nhỏ. Sau mỗi phase, kiểm tra file đã sửa, chạy ứng dụng/test và xác minh kết quả trước khi chuyển tiếp.

### Phase A — Inspect và lập kế hoạch nhanh

- Đọc repository và tuân thủ convention hiện có.
- Xác định lệnh chạy, dependencies và cấu trúc hiện tại.
- Kiểm tra các yêu cầu Meta API dựa trên tài liệu chính thức hiện hành.
- Xác định một objective và một format quảng cáo duy nhất cho MVP.
- Liệt kê cấu hình/permissions còn thiếu.
- Không viết kiến trúc dư thừa hoặc tạo nhiều tài liệu không cần thiết.

### Phase B — Skeleton và OAuth

- Hoàn thiện Next.js + TypeScript + Tailwind và FastAPI.
- Tạo health endpoint.
- Thêm cấu hình môi trường và validation.
- Implement OAuth, state validation, callback và token handling ở backend.
- Verify kết quả kết nối trước khi xây form tạo quảng cáo.

### Phase C — Meta account/Page

- Implement endpoint lấy ad accounts.
- Implement endpoint lấy Pages.
- Hiển thị danh sách thật ở frontend.
- Test các trường hợp danh sách rỗng/thiếu quyền.

### Phase D — Tạo quảng cáo

- Implement đúng chuỗi API cần thiết cho một objective/format.
- Mặc định `PAUSED` nếu được hỗ trợ.
- Validate form và ngân sách.
- Ngăn double-submit.
- Hiển thị IDs và lỗi theo từng bước; không giả lập success.

### Phase E — Demo hardening

- Chạy luồng từ đầu đến cuối.
- Kiểm tra logs không chứa token/secret.
- Kiểm tra trạng thái quảng cáo và ngân sách trước khi demo.
- Hoàn thiện README và demo checklist.
- Không thêm feature mới khi chưa hoàn thành luồng end-to-end.

## 16. Prompt triển khai chính cho Antigravity

Dùng prompt dưới đây làm chỉ dẫn ban đầu; sau đó giao từng phase cụ thể thay vì yêu cầu agent làm toàn bộ trong một lần.

> You are a pragmatic senior full-stack engineer. Build a minimal but real end-to-end MVP named **BAHA Ads Manager** under a strict two-hour time limit.
>
> **Stack:** Next.js, TypeScript, Tailwind CSS; FastAPI; SQLite; official Meta Graph API / Marketing API.
>
> **Primary acceptance goal:** A user can connect Facebook through Meta OAuth, select an accessible ad account and Facebook Page, enter product-ad details, submit the form, and see the actual response/resource IDs from Meta after the backend attempts to create the required advertising resources.
>
> Requirements:
> 1. Inspect the existing repository first and reuse its conventions where possible.
> 2. Prioritize the smallest working end-to-end path. Do not overengineer or add unrelated features.
> 3. Use official Meta API documentation to verify current endpoints, permissions, fields, API version, and required resource creation order. Do not invent API capabilities or payload fields.
> 4. Keep App Secret and access tokens on the backend. Never expose credentials in frontend responses, source control, or logs. Validate OAuth `state`.
> 5. Load real ad accounts and Pages accessible to the connected user. Never hardcode BAHA account IDs.
> 6. Support one verified campaign objective and one ad format only. Use a minimal form for account, Page, campaign/ad names, budget, copy, destination URL, and image if required.
> 7. Create resources using the real Meta Marketing API. Default to `PAUSED` where supported. Do not claim that an ad is approved or delivering unless the API confirms that state.
> 8. Handle partial failures and timeouts honestly. Do not automatically retry create operations when the outcome is uncertain, because duplicate resources may be created.
> 9. Use SQLite only for minimal persistence if needed. Skip Insights, charts, advanced targeting, AI copywriting, and extra features until the end-to-end path works.
> 10. Provide clear loading, empty, success, and error states. A mock mode, if used for isolated UI work, must be explicitly labeled and must never be presented as real Meta integration.
> 11. Add a concise README with setup, environment variables, Meta app prerequisites, run commands, and demo steps.
> 12. After each phase, run the relevant checks and report changed files, actual verification results, blockers, and next steps.
>
> Work in this order: (A) inspect repo and confirm Meta prerequisites; (B) skeleton and OAuth; (C) fetch/select ad account and Page; (D) create one real ad flow; (E) verify the demo path and document blockers.
>
> **Do not spend time on elaborate architecture or polishing. Do not state that the task is complete unless the real integration has been verified. If Meta credentials, permissions, app review, account eligibility, or payment setup block publishing, report the exact blocker and do not fake success.**

## 17. Demo checklist ngay trước khi trình bày

- [ ] Kiểm tra backend/frontend đều đang chạy.
- [ ] Kiểm tra `.env` và callback URL.
- [ ] Đăng nhập bằng đúng tài khoản BAHA cung cấp.
- [ ] Chọn đúng ad account và Page.
- [ ] Kiểm tra URL sản phẩm, nội dung, ảnh và ngân sách.
- [ ] Đảm bảo status ban đầu đúng yêu cầu demo; tránh vô tình bật chi tiêu.
- [ ] Nhấn tạo một lần và chờ response.
- [ ] Chụp/ghi lại resource IDs, status hoặc lỗi thật.
- [ ] Mở danh sách campaign và refresh từ Meta nếu có thể.
- [ ] Không tuyên bố quảng cáo đã được duyệt/phân phối nếu chỉ mới tạo resource.

---

## Nguyên tắc quyết định

Trong giới hạn 2 giờ, **một luồng thật chạy được tốt hơn một dashboard đẹp nhưng không thể tạo quảng cáo**. Điểm rủi ro lớn nhất không phải Next.js, FastAPI hay SQLite, mà là Meta App, OAuth, quyền quảng cáo, quyền Page và điều kiện của ad account. Xác minh các điều kiện này ngay từ đầu; nếu chúng chưa sẵn sàng, phải báo rõ blocker thay vì dùng dữ liệu giả để tạo ấn tượng rằng quảng cáo đã được đăng.
