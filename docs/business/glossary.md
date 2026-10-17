# Domain Glossary — BAHA Ads Manager

**Document Layer**: Business Layer  
**Version**: 1.0  
**Date**: 2026-10-17  
**Status**: Active  

---

## 1. Thuật ngữ nền tảng Meta Ads (Meta Advertising Concepts)

| Thuật ngữ | Tên tiếng Anh | Định nghĩa & Ý nghĩa nghiệp vụ |
|---|---|---|
| **Tài khoản quảng cáo** | Ad Account | Thực thể quản lý tài chính, phương thức thanh toán và các chiến dịch quảng cáo trên nền tảng Meta (định dạng ID: `act_<account_id>`). |
| **Trang Facebook** | Facebook Page / Fanpage | Danh tính đại diện thương hiệu hoặc doanh nghiệp xuất hiện trên bài viết quảng cáo. Bắt buộc phải có để tạo bài quảng cáo. |
| **Chiến dịch** | Campaign | Cấp độ cao nhất trong cấu trúc quảng cáo Meta, xác định mục tiêu tổng thể (Objective) của nhà quảng cáo. |
| **Nhóm quảng cáo** | Ad Set | Cấp độ thứ hai, xác định ngân sách (Budget), lịch chạy, đối tượng mục tiêu (Targeting), vị trí hiển thị và sự kiện tối ưu hóa. |
| **Mẫu quảng cáo** | Ad Creative | Nội dung hình ảnh, video, văn bản, tiêu đề, liên kết đích và nút kêu gọi hành động (CTA) mà người dùng Facebook nhìn thấy. |
| **Quảng cáo** | Ad | Cấp độ thực thi cuối cùng, liên kết một Nhóm quảng cáo với một Mẫu quảng cáo để Meta tiến hành phân phối. |
| **Mục tiêu chiến dịch** | Campaign Objective | Định hướng thuật toán phân phối của Meta. Trong MVP chốt là `OUTCOME_TRAFFIC` (kéo lưu lượng truy cập về website). |
| **Đơn vị tiền tệ** | Currency Multiplier | Quy chuẩn xử lý ngân sách của Meta: Với đồng tiền có cent (USD, EUR,...), ngân sách gửi lên API phải nhân 100; với đồng tiền không có số thập phân (VND, JPY), ngân sách giữ nguyên số nguyên. |
| **Mã băm hình ảnh** | Image Hash | Chuỗi băm nhận diện duy nhất do Meta sinh ra sau khi tải hình ảnh lên endpoint `/adimages`, dùng để gắn vào Ad Creative. |

---

## 2. Thuật ngữ kỹ thuật & Vận hành nội bộ (System Concepts)

| Thuật ngữ | Ý nghĩa trong hệ thống BAHA Ads Manager |
|---|---|
| **Session** | Phiên làm việc lưu trữ token xác thực Meta của người dùng thao tác trong bảng SQLite `meta_sessions`. |
| **Creation Run** | Một bản ghi lưu lại vết thực thi của tiến trình tạo quảng cáo trong bảng `ad_creation_runs`, ghi nhận trạng thái và ID của từng tài nguyên sinh ra. |
| **Trạng thái PAUSED** | Trạng thái tạm dừng mặc định khi tạo mới tài nguyên trên Meta để bảo đảm an toàn, không kích hoạt chi tiêu ngoài ý muốn. |
| **Partial Failure** | Tình trạng một số tài nguyên ban đầu được tạo thành công (ví dụ Campaign, Ad Set) nhưng bước tiếp theo (Creative hoặc Ad) thất bại. Hệ thống bắt buộc phải hiển thị rõ các ID đã tạo thay vì báo thất bại trắng. |
