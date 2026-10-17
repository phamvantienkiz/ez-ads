# Technical Design Document — Release 1: MVP Demo

**Tầng tài liệu**: Implementation Layer  
**Release**: release-1 (MVP Demo)  
**Tài liệu tham chiếu**: [prd.md](prd.md), [02-high-level-architecture.md](../../architecture/02-high-level-architecture.md), [08-integration-architecture.md](../../architecture/08-integration-architecture.md)  
**Ngày phê duyệt**: 2026-10-17  
**Trạng thái**: Approved  

---

## 1. Subsystem Scope & Technical Goals

Tài liệu này đặc tả chi tiết kiến trúc kỹ thuật nội bộ của **Release 1 (MVP Demo)**, tập trung vào hai luồng nghiệp vụ xương sống:
1. **Luồng Xác thực & Kết nối Tài sản (Auth & Asset Ingestion Flow)**.
2. **Luồng Điều phối Tạo Quảng cáo Tuần tự (Sequential Ad Creation Flow)**.

---

## 2. Detailed Technical Sequence Diagrams

### 2.1. Luồng Xác thực OAuth 2.0 & Duy trì Phiên
```mermaid
sequenceDiagram
    autonumber
    actor User as BAHA Demo Operator
    participant UI as Next.js Client (:3000)
    participant AuthRouter as FastAPI Auth Router
    participant AuthService as MetaAuthService
    participant SessionRepo as SessionRepository (SQLite)
    participant MetaOAuth as Meta OAuth Platform

    User->>UI: Bấm "Connect Facebook"
    UI->>AuthRouter: GET /api/meta/connect
    AuthRouter->>AuthService: generate_oauth_url()
    Note over AuthService: Sinh ngẫu nhiên cryptographically secure state<br/>Lưu state vào memory/cookie
    AuthService-->>AuthRouter: Trả về URL: https://www.facebook.com/v20.0/dialog/oauth?...
    AuthRouter-->>UI: 302 Redirect hoặc JSON trả về OAuth URL
    UI->>MetaOAuth: Chuyển hướng người dùng sang Facebook Login
    MetaOAuth->>User: Yêu cầu cấp quyền: ads_management, ads_read, pages_manage_ads...
    User->>MetaOAuth: Đồng ý cấp quyền
    MetaOAuth->>AuthRouter: GET /api/meta/callback?code={auth_code}&state={state}
    
    AuthRouter->>AuthService: handle_callback(code, state)
    Note over AuthService: Xác minh state khớp giá trị ban đầu (CSRF check)
    AuthService->>MetaOAuth: POST /v20.0/oauth/access_token (code, app_secret)
    MetaOAuth-->>AuthService: Trả về {access_token, token_type, expires_in}
    
    AuthService->>SessionRepo: save_session(access_token, expires_in)
    Note over SessionRepo: INSERT OR REPLACE INTO meta_sessions (id=1, ...)
    SessionRepo-->>AuthService: OK
    
    AuthRouter-->>UI: 302 Redirect về http://localhost:3000/?connected=true
    UI->>AuthRouter: GET /api/meta/status
    AuthRouter-->>UI: {"success": true, "data": {"connected": true}}
    UI->>User: Hiển thị trạng thái "Đã kết nối Meta"
```

---

### 2.2. Luồng Điều phối Chuỗi 5 Lời gọi Meta Marketing API
```mermaid
sequenceDiagram
    autonumber
    actor User as BAHA Demo Operator
    participant UI as Next.js Client (:3000)
    participant AdsRouter as FastAPI Ads Router
    participant AdService as AdCreationService
    participant MetaClient as MetaClientService (httpx)
    participant RunRepo as RunRepository (SQLite)
    participant MetaAPI as Meta Marketing API v20.0

    User->>UI: Điền Form & Xem Preview -> Bấm "Xác nhận tạo quảng cáo"
    Note over UI: Khóa nút submit (isSubmitting = true)
    UI->>AdsRouter: POST /api/ads (Payload đầy đủ các trường)
    AdsRouter->>AdService: create_ad_pipeline(payload)
    
    AdService->>RunRepo: create_run(status='pending', summary=payload)
    RunRepo-->>AdService: run_id
    
    %% Bước 1
    rect rgb(240, 248, 255)
    Note over AdService, MetaAPI: Bước 1: Upload & Băm hình ảnh
    AdService->>MetaClient: upload_image_url(ad_account_id, image_url)
    MetaClient->>MetaAPI: POST /act_{id}/adimages (url={image_url})
    MetaAPI-->>MetaClient: {"images": {"{url}": {"hash": "img_hash_123"}}}
    MetaClient-->>AdService: image_hash
    end

    %% Bước 2
    rect rgb(245, 255, 245)
    Note over AdService, MetaAPI: Bước 2: Tạo Campaign
    AdService->>MetaClient: create_campaign(ad_account_id, name, objective='OUTCOME_TRAFFIC', status='PAUSED')
    MetaClient->>MetaAPI: POST /act_{id}/campaigns
    MetaAPI-->>MetaClient: {"id": "cmp_101"}
    MetaClient-->>AdService: campaign_id
    AdService->>RunRepo: update_run(run_id, campaign_id="cmp_101")
    end

    %% Bước 3
    rect rgb(255, 250, 240)
    Note over AdService, MetaAPI: Bước 3: Tạo Ad Set (kèm quy đổi ngân sách)
    Note over AdService: format_meta_budget(budget, currency)
    AdService->>MetaClient: create_adset(ad_account_id, campaign_id, formatted_budget, targeting, status='PAUSED')
    MetaClient->>MetaAPI: POST /act_{id}/adsets
    MetaAPI-->>MetaClient: {"id": "adset_202"}
    MetaClient-->>AdService: adset_id
    AdService->>RunRepo: update_run(run_id, adset_id="adset_202")
    end

    %% Bước 4
    rect rgb(255, 245, 255)
    Note over AdService, MetaAPI: Bước 4: Tạo Ad Creative
    AdService->>MetaClient: create_creative(ad_account_id, page_id, headline, primary_text, link, image_hash)
    MetaClient->>MetaAPI: POST /act_{id}/adcreatives
    MetaAPI-->>MetaClient: {"id": "cre_303"}
    MetaClient-->>AdService: creative_id
    AdService->>RunRepo: update_run(run_id, creative_id="cre_303")
    end

    %% Bước 5
    rect rgb(240, 255, 255)
    Note over AdService, MetaAPI: Bước 5: Tạo Ad Hoàn chỉnh
    AdService->>MetaClient: create_ad(ad_account_id, adset_id, creative_id, name, status='PAUSED')
    MetaClient->>MetaAPI: POST /act_{id}/ads
    MetaAPI-->>MetaClient: {"id": "ad_404"}
    MetaClient-->>AdService: ad_id
    AdService->>RunRepo: update_run(run_id, ad_id="ad_404", status='success')
    end

    AdService-->>AdsRouter: CreationResult(success=True, IDs={...})
    AdsRouter-->>UI: HTTP 201 Created {"success": true, "data": {...}}
    UI->>User: Hiển thị Panel kết quả thật (Campaign ID, Ad Set ID, Creative ID, Ad ID)
```

---

## 3. Partial Failure Handling & Recovery Flow

Nếu xảy ra lỗi tại bất kỳ bước nào trong chuỗi 5 bước (ví dụ: bước 4 tạo Creative bị lỗi do link đích bị Meta chặn):
1. `AdCreationService` bắt exception cụ thể từ `MetaClient`.
2. Trích xuất mã lỗi và thông báo lỗi đã được làm sạch qua `sanitize_meta_error()`.
3. Cập nhật bản ghi `ad_creation_runs` với `status = 'partial_failure'`, lưu lại các ID đã tạo thành công trước đó (ví dụ: `campaign_id` và `adset_id`) và lưu `error_message`.
4. Trả về HTTP 207 Multi-Status hoặc HTTP 400 kèm chi tiết:
   ```json
   {
     "success": false,
     "status": "partial_failure",
     "created_resources": {
       "campaign_id": "120210000000001",
       "adset_id": "120210000000002",
       "creative_id": null,
       "ad_id": null
     },
     "failed_step": "create_creative",
     "error": {
       "code": "META_CREATIVE_POLICY_VIOLATION",
       "message": "Trang đích sản phẩm không thể truy cập hoặc vi phạm tiêu chuẩn Meta."
     }
   }
   ```
5. Giao diện hiển thị rõ ràng các tài nguyên đã tạo, bước bị lỗi, và **tuyệt đối không tự động retry**.
