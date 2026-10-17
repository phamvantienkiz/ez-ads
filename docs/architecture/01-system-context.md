# 01. System Context & Use Case Scope — BAHA Ads Manager

**Document Layer**: Architecture Layer  
**Version**: 1.0  
**Date**: 2026-10-17  
**Status**: Living Architecture (Single Source of Truth)  

---

## 1. System Boundary & Actors

Hệ thống **BAHA Ads Manager** hoạt động như một ứng dụng web nội bộ hỗ trợ kết nối và điều phối tạo tài nguyên quảng cáo trực tiếp thông qua **Meta Graph & Marketing API**.

### 1.1. Hệ thống tác nhân (Actors)
- **👤 BAHA Demo Operator**: Người đại diện BAHA trực tiếp thao tác trên trình duyệt, sở hữu tài khoản Facebook có quyền truy cập vào Ad Account và Fanpage thử nghiệm.
- **🌐 Meta OAuth Service**: Dịch vụ xác thực danh tính và phân quyền của Facebook, cung cấp Authorization Code để backend quy đổi Access Token.
- **🌐 Meta Marketing API**: Cụm API chính thức của Meta Platforms (`v20.0`), cung cấp các endpoints tải tài sản, upload ảnh và tạo Campaign/Ad Set/Creative/Ad.
- **💾 Local SQLite Database**: Cơ sở dữ liệu cục bộ lưu trữ phiên làm việc an toàn (`meta_sessions`) và lịch sử thực thi (`ad_creation_runs`).

---

## 2. Use Case Diagram (System Boundary)

```mermaid
flowchart LR
    subgraph Actors ["Tác nhân (Actors)"]
        User["👤 BAHA Operator"]
        MetaAuth["🌐 Meta OAuth Gateway"]
        MetaAPI["🌐 Meta Marketing API"]
    end

    subgraph SystemBoundary ["BAHA Ads Manager System Boundary"]
        UC1["(1. Kết nối tài khoản Meta)"]
        UC2["(2. Chọn Ad Account & Fanpage)"]
        UC3["(3. Nhập cấu hình quảng cáo sản phẩm)"]
        UC4["(4. Xem trước & Xác nhận an toàn)"]
        UC5["(5. Gọi Meta API tạo tài nguyên)"]
        UC6["(6. Xem kết quả thật & Bảng chiến dịch)"]
        
        UC1 -.->|<<include>>| UC2
        UC3 -.->|<<include>>| UC4
        UC4 -.->|<<include>>| UC5
    end

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC6

    UC1 <-->|Trao đổi mã OAuth & Token| MetaAuth
    UC2 <-->|Tải Ad Accounts & Pages| MetaAPI
    UC5 <-->|Chuỗi tạo: Image/Campaign/AdSet/Creative/Ad| MetaAPI
    UC6 <-->|Truy vấn danh sách Campaigns| MetaAPI
```

---

## 3. End-to-End Business Workflow

```mermaid
flowchart TD
    Start([Bắt đầu phiên làm việc]) --> ConnectMeta[Người dùng nhấn 'Connect Facebook']
    ConnectMeta --> OAuthRedirect[Backend tạo URL OAuth + State và chuyển hướng người dùng]
    OAuthRedirect --> AuthConsent{Người dùng xác nhận cấp quyền trên Facebook?}
    AuthConsent -- Từ chối/Lỗi --> DisplayAuthErr[Hiển thị lỗi xác thực và cho phép thử lại]
    DisplayAuthErr --> ConnectMeta
    AuthConsent -- Đồng ý --> CallbackHandling[Backend tiếp nhận Callback, verify state và lấy Token]
    
    CallbackHandling --> FetchAssets[Backend truy vấn danh sách Ad Accounts và Pages]
    FetchAssets --> SelectAssets[Người dùng chọn 1 Ad Account và 1 Page đại diện]
    SelectAssets --> FillAdForm[Người dùng nhập nội dung sản phẩm, URL đích, ảnh và ngân sách]
    FillAdForm --> PreviewConfirm[Hiển thị Preview và Tóm tắt cấu hình an toàn]
    
    PreviewConfirm --> UserSubmit{Người dùng bấm nút xác nhận tạo quảng cáo?}
    UserSubmit -- Chỉnh sửa --> FillAdForm
    UserSubmit -- Xác nhận --> CallMetaAPI[Backend thực thi chuỗi gọi Meta Marketing API theo thứ tự]
    
    CallMetaAPI --> Step1Image[1. Upload/Hash Image URL lấy image_hash]
    Step1Image --> Step2Campaign[2. Tạo Campaign OUTCOME_TRAFFIC status PAUSED]
    Step2Campaign --> Step3AdSet[3. Tạo Ad Set ngân sách quy đổi và targeting mặc định]
    Step3AdSet --> Step4Creative[4. Tạo Ad Creative liên kết Fanpage và Link sản phẩm]
    Step4Creative --> Step5Ad[5. Tạo Ad gắn Ad Set và Creative]
    
    Step5Ad --> SaveRunDB[Lưu kết quả chi tiết từng tài nguyên vào SQLite ad_creation_runs]
    SaveRunDB --> DisplayRealResult[Giao diện hiển thị ID và trạng thái thật từ Meta]
    DisplayRealResult --> RefreshCampaigns[Người dùng xem bảng điều khiển các chiến dịch trên tài khoản]
    RefreshCampaigns --> End([Kết thúc luồng demo])
```

---

## 4. Ranh giới hệ thống (Scope Boundaries)

- **Phần mềm chịu trách nhiệm**:
  - Quản lý phiên OAuth bảo mật phía server, không để lộ Secret hay Token về phía client.
  - Kiểm tra tính hợp lệ của dữ liệu đầu vào (URL, độ lớn ngân sách, tiền tệ theo tài khoản).
  - Điều phối chuỗi 5 lời gọi Meta Marketing API tuần tự, ghi nhận chính xác kết quả từng bước (ngay cả khi xảy ra lỗi một phần - Partial Failure).
- **Phần mềm không chịu trách nhiệm**:
  - Không chịu trách nhiệm về chính sách phê duyệt bài quảng cáo hoặc xử lý tài khoản bị hạn chế thanh toán của Meta.
  - Không quản lý việc nạp tiền hoặc giải quyết tranh chấp tài khoản với Facebook.
