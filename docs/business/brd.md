# Business Requirements Document (BRD) — BAHA Ads Manager

**Document Layer**: Business Layer  
**Version**: 1.0  
**Date**: 2026-10-17  
**Status**: Approved  

---

## 1. Executive Summary & Business Context

BAHA cần một ứng dụng nội bộ hỗ trợ thao tác tạo và quản lý quảng cáo sản phẩm trên nền tảng Meta (Facebook/Instagram). Để đáp ứng nhu cầu chứng minh năng lực công nghệ và kiểm chứng quy trình tích hợp API trong thời gian gấp, dự án tập trung phát triển giải pháp **BAHA Ads Manager** nhằm tự động hóa luồng kết nối tài khoản Meta, lựa chọn tài sản số (Ad Account, Fanpage) và gửi trực tiếp dữ liệu tạo chiến dịch quảng cáo thông qua **Meta Marketing API chính thức**.

Mục tiêu chiến lược là xây dựng một nền tảng vận hành chuẩn mực, loại bỏ các thao tác thủ công phức tạp trên Meta Ads Manager truyền thống, đồng thời đảm bảo an toàn tài chính (ngân sách), dữ liệu trung thực 100% từ API thật, và tuân thủ các chính sách của Meta.

---

## 2. Business Problem & Opportunity

### 2.1. Vấn đề thực tế (Pain Points)
- **Thao tác thủ công cồng kềnh**: Việc tạo chiến dịch quảng cáo trực tiếp trên trình quản lý của Facebook đòi hỏi nhiều bước cấu hình phức tạp, dễ gây nhầm lẫn về ngân sách, đối tượng và tài khoản phân phối.
- **Rủi ro gián đoạn và sai lệch cấu hình**: Nhân sự thao tác có thể cấu hình sai múi giờ, loại tiền tệ (currency multiplier) hoặc để chiến dịch tự động kích hoạt chi tiêu ngoài ý muốn.
- **Nhu cầu kiểm chứng tích hợp thực tế**: Doanh nghiệp cần xác minh khả năng kết nối trực tiếp với Meta Marketing API end-to-end, kiểm chứng cơ chế OAuth phân quyền và trả về kết quả thật (ID, trạng thái) thay vì các bản mô phỏng giao diện tĩnh.

### 2.2. Cơ hội kinh doanh & Giá trị mang lại (ROI)
- **Rút ngắn thời gian triển khai**: Giảm thiểu 70% thời gian thiết lập một chiến dịch quảng cáo tiêu chuẩn cho sản phẩm.
- **Kiểm soát an toàn ngân sách tuyệt đối**: Mặc định đặt trạng thái chiến dịch là `PAUSED` khi tạo mới, ngăn chặn việc phát sinh chi phí ngoài dự kiến trước khi có phê duyệt.
- **Nền tảng mở rộng linh hoạt**: Tạo tiền đề để tích hợp sâu hơn các công nghệ tự động hóa, báo cáo số liệu hiệu quả (Insights), và AI tối ưu hóa quảng cáo ở các giai đoạn sau.

---

## 3. Business Goals & Success Metrics (KPIs)

| Chỉ số (KPI) | Mục tiêu cơ sở (Baseline) | Mục tiêu MVP (Target) | Phương thức đo lường |
|---|---|---|---|
| **End-to-End Flow Success** | 0% (chưa có hệ thống) | 100% hoàn thành luồng từ OAuth đến trả kết quả thật từ Meta | Kiểm tra nhật ký tạo tài nguyên trong bảng `ad_creation_runs` |
| **API Data Integrity** | Dữ liệu giả lập / mock | 100% dữ liệu tài khoản, page, kết quả tạo là từ Meta Graph API thật | Đối soát `campaign_id`, `adset_id`, `ad_id` trên Meta Ads Manager |
| **Safety Compliance** | Không có cơ chế chặn chi tiêu tự động | 100% tài nguyên tạo ra mặc định ở trạng thái `PAUSED` | Kiểm tra trạng thái status gửi lên Meta và lưu DB |
| **Thời gian tạo quảng cáo** | 10-15 phút thao tác thủ công | < 2 phút qua giao diện biểu mẫu tối giản | Thời gian hoàn tất form và nhận phản hồi |

---

## 4. Business Scope Boundary

### 4.1. In-Scope (Thuộc phạm vi kinh doanh cốt lõi)
- Xác thực kết nối tài khoản Facebook qua OAuth bảo mật ở backend.
- Lấy danh sách Ad Account và Facebook Fanpage mà tài khoản được cấp quyền truy cập hợp lệ.
- Cung cấp biểu mẫu chuẩn hóa tạo quảng cáo sản phẩm với mục tiêu cố định `OUTCOME_TRAFFIC` và định dạng `Single Image Link Ad`.
- Quản lý quy đổi tiền tệ chính xác theo đơn vị Ad Account (cent vs integer).
- Xem trước nội dung quảng cáo và xác nhận an toàn trước khi kích hoạt gọi API.
- Tạo tuần tự chuỗi 5 tài nguyên Meta (Image Hash -> Campaign -> Ad Set -> Ad Creative -> Ad) và ghi nhận kết quả thật.
- Bảng điều khiển vận hành tối giản hiển thị danh sách chiến dịch và lịch sử tạo gần nhất.

### 4.2. Out-of-Scope (Ngoại phạm vi giai đoạn đầu)
- Hệ thống tài khoản người dùng nội bộ (RBAC phân quyền đa tổ chức).
- Thanh toán, quản lý hóa đơn, nạp tiền vào tài khoản Meta.
- AI sinh nội dung, A/B Testing, tối ưu hóa giá thầu tự động.
- Quản lý kho media phức tạp hoặc tải lên nhiều ảnh/video cùng lúc.
- Lập lịch phát hành chiến dịch nhiều cấp phê duyệt.

---

## 5. Domain Modules & Business Boundaries

```
┌────────────────────────────────────────────────────────┐
│                   BAHA ADS MANAGER                     │
├───────────────────┬───────────────────┬────────────────┤
│  Identity & Auth  │ Asset Selection   │ Campaign Ops   │
│  - Meta OAuth     │ - Ad Accounts     │ - Traffic Form │
│  - Session State  │ - Managed Pages   │ - Meta API Run │
└───────────────────┴───────────────────┴────────────────┘
```

1. **Phân hệ Kết nối & Định danh (Identity & Auth)**: Quản lý vòng đời kết nối với Meta, trao đổi mã xác thực, lưu trữ session an toàn ở server.
2. **Phân hệ Tài sản số (Asset Selection)**: Truy vấn và cho phép lựa chọn tài khoản quảng cáo đủ điều kiện và Fanpage đại diện thương hiệu.
3. **Phân hệ Vận hành Chiến dịch (Campaign Operations)**: Xử lý dữ liệu sản phẩm, kiểm tra tính hợp lệ của ngân sách, tạo và đồng bộ tài nguyên với Meta Marketing API.
