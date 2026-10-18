'use client';

import React, { useState } from 'react';
import { CreateAdPayload, AdAccount } from '@/types';
import { ShieldCheck, AlertCircle, Loader2, Sparkles } from 'lucide-react';

interface AdFormProps {
  initialValues: CreateAdPayload;
  selectedAccount?: AdAccount;
  selectedPageId?: string;
  isSubmitting: boolean;
  errorMessage?: string | null;
  onChange: (values: CreateAdPayload) => void;
  onSubmit: (values: CreateAdPayload) => void;
  onPublishPagePost?: (values: CreateAdPayload) => void;
}

export function AdForm({
  initialValues,
  selectedAccount,
  selectedPageId,
  isSubmitting,
  errorMessage,
  onChange,
  onSubmit,
  onPublishPagePost,
}: AdFormProps) {
  const [validationError, setValidationError] = useState<string | null>(null);

  const currency = selectedAccount?.currency || 'VND';

  const handleChange = (field: keyof CreateAdPayload, value: any) => {
    const updated = { ...initialValues, [field]: value };
    onChange(updated);
    if (validationError) setValidationError(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!initialValues.campaignName.trim()) {
      setValidationError('Vui lòng nhập tên chiến dịch.');
      return;
    }
    if (!initialValues.budgetAmount || initialValues.budgetAmount <= 0) {
      setValidationError('Vui lòng nhập ngân sách hợp lệ (> 0).');
      return;
    }
    if (!initialValues.headline.trim()) {
      setValidationError('Vui lòng nhập tiêu đề quảng cáo.');
      return;
    }
    if (!initialValues.primaryText.trim()) {
      setValidationError('Vui lòng nhập nội dung chính của bài quảng cáo.');
      return;
    }
    if (!initialValues.destinationUrl.trim().startsWith('http')) {
      setValidationError('URL trang đích phải bắt đầu bằng http:// hoặc https://');
      return;
    }
    if (!initialValues.imageUrl.trim().startsWith('http')) {
      setValidationError('URL hình ảnh phải bắt đầu bằng http:// hoặc https://');
      return;
    }

    setValidationError(null);
    onSubmit(initialValues);
  };

  const handlePagePostClick = () => {
    if (!initialValues.headline.trim()) {
      setValidationError('Vui lòng nhập tiêu đề bài viết.');
      return;
    }
    if (!initialValues.primaryText.trim()) {
      setValidationError('Vui lòng nhập nội dung chính của bài viết.');
      return;
    }
    if (!initialValues.destinationUrl.trim().startsWith('http')) {
      setValidationError('URL trang đích phải bắt đầu bằng http:// hoặc https://');
      return;
    }
    setValidationError(null);
    if (onPublishPagePost) {
      onPublishPagePost(initialValues);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      {/* Form Title & Subtitle */}
      <div>
        <h2 className="text-[22px] font-semibold text-primary tracking-tight">
          Tạo chiến dịch quảng cáo mới
        </h2>
        <p className="text-[13px] text-muted mt-1">
          Thiết lập thông tin bài viết link sản phẩm gửi tới Meta Marketing API.
        </p>
      </div>

      {/* Error Alert Banner */}
      {(validationError || errorMessage) && (
        <div className="bg-[#FFF0F2] border border-[#FDD0D5] text-[#E5483D] px-4 py-3 rounded-xl text-[13px] flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <div className="leading-snug">
            {validationError || errorMessage}
          </div>
        </div>
      )}

      {/* Field: Campaign Name */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          Tên chiến dịch <span className="text-data-alert">*</span>
        </label>
        <input
          type="text"
          value={initialValues.campaignName}
          onChange={(e) => handleChange('campaignName', e.target.value)}
          placeholder="Ví dụ: BAHA Polo Shirt Traffic Campaign"
          disabled={isSubmitting}
          className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft"
        />
      </div>

      {/* Field: Daily Budget with Currency Badge */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          Ngân sách hàng ngày (Daily Budget) <span className="text-data-alert">*</span>
        </label>
        <div className="relative flex items-center">
          <input
            type="number"
            min={1}
            step={currency === 'USD' ? 1 : 1000}
            value={initialValues.budgetAmount || ''}
            onChange={(e) => handleChange('budgetAmount', Number(e.target.value))}
            placeholder={currency === 'USD' ? '10' : '50000'}
            disabled={isSubmitting}
            className="w-full bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] tabular-nums rounded-xl pl-3.5 pr-20 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all"
          />
          <div className="absolute right-2 px-2.5 py-1 bg-white border border-border-card text-[12px] font-semibold text-primary rounded-lg shadow-sm">
            {currency}
          </div>
        </div>
        <span className="text-[11px] text-muted-soft">
          {currency === 'USD' || currency === 'EUR'
            ? 'Backend tự động nhân 100 theo chuẩn cent của Meta API'
            : 'Backend giữ nguyên số nguyên theo chuẩn tiền tệ không có cent (VND)'}
        </span>
      </div>

      {/* Field: Headline */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          Tiêu đề bài viết (Headline) <span className="text-data-alert">*</span>
        </label>
        <input
          type="text"
          value={initialValues.headline}
          onChange={(e) => handleChange('headline', e.target.value)}
          placeholder="Ví dụ: Áo Polo Nam Cao Cấp BAHA"
          disabled={isSubmitting}
          className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft"
        />
      </div>

      {/* Field: Primary Text */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          Nội dung văn bản chính (Primary Text) <span className="text-data-alert">*</span>
        </label>
        <textarea
          rows={3}
          value={initialValues.primaryText}
          onChange={(e) => handleChange('primaryText', e.target.value)}
          placeholder="Trải nghiệm dòng áo Polo nam cao cấp từ BAHA với chất liệu thoáng mát vượt trội..."
          disabled={isSubmitting}
          className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft resize-none"
        />
      </div>

      {/* Field: Destination URL */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          URL trang đích sản phẩm (Destination URL) <span className="text-data-alert">*</span>
        </label>
        <input
          type="url"
          value={initialValues.destinationUrl}
          onChange={(e) => handleChange('destinationUrl', e.target.value)}
          placeholder="https://baha.vn/products/polo-classic"
          disabled={isSubmitting}
          className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft"
        />
      </div>

      {/* Field: Image URL */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[13px] font-medium text-muted">
          URL hình ảnh sản phẩm (Public Image URL) <span className="text-data-alert">*</span>
        </label>
        <input
          type="url"
          value={initialValues.imageUrl}
          onChange={(e) => handleChange('imageUrl', e.target.value)}
          placeholder="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800"
          disabled={isSubmitting}
          className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[14px] rounded-xl px-3.5 py-2.5 border border-transparent focus:border-border-card focus:outline-none transition-all placeholder:text-muted-soft"
        />
        <span className="text-[11px] text-muted-soft">
          Ảnh phải truy cập công khai để Meta Marketing API tải về và sinh image hash.
        </span>
      </div>

      {/* Fixed Settings Info Box */}
      <div className="bg-subtle rounded-xl p-3 border border-border-hairline grid grid-cols-2 sm:grid-cols-3 gap-2 text-[12px]">
        <div>
          <span className="text-muted-soft block text-[10px] uppercase font-semibold">Mục tiêu</span>
          <span className="font-medium text-primary">OUTCOME_TRAFFIC</span>
        </div>
        <div>
          <span className="text-muted-soft block text-[10px] uppercase font-semibold">Targeting</span>
          <span className="font-medium text-primary">Việt Nam (18–65)</span>
        </div>
        <div>
          <span className="text-muted-soft block text-[10px] uppercase font-semibold">Kêu gọi CTA</span>
          <span className="font-medium text-primary">LEARN_MORE</span>
        </div>
      </div>

      {/* Budget Safety Warning Box (Mandatory Invariant) */}
      <div className="bg-[#FFF1C9] border border-[#FFE494] text-[#8C5200] p-4 rounded-xl text-[13px] flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-[#FF8A1F] shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold text-[#663E00]">
            Cơ chế bảo vệ ngân sách an toàn (Safety Invariant)
          </p>
          <p className="text-[12px] text-[#7A4B00] mt-0.5">
            Chiến dịch và Ad Set sẽ luôn được tạo ở trạng thái <strong className="font-semibold">TẠM DỪNG (PAUSED)</strong>. Hệ thống tuyệt đối không tự động kích hoạt chi tiêu quảng cáo.
          </p>
        </div>
      </div>

      {/* Submit Primary Ink Button */}
      <div className="flex flex-col gap-2.5 mt-2">
        <button
          type="submit"
          disabled={isSubmitting || !selectedAccount}
          className="w-full bg-ink hover:bg-black text-white text-[14px] font-medium py-3.5 px-6 rounded-xl shadow-primary transition-all duration-150 active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin text-white" />
              <span>Đang thực thi trên Meta API...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-white" />
              <span>Xác nhận tạo quảng cáo trên Meta (5 bước)</span>
            </>
          )}
        </button>

        {onPublishPagePost && (
          <button
            type="button"
            onClick={handlePagePostClick}
            disabled={isSubmitting || (!selectedPageId && !initialValues.pageId)}
            className="w-full bg-subtle hover:bg-[#E5E5EA] text-primary text-[13px] font-medium py-2.5 px-4 rounded-xl border border-border-card transition-all active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span>Dự phòng Demo: Đăng bài Post trực tiếp lên Fanpage (Không qua trình quản lý Ads)</span>
          </button>
        )}
      </div>
    </form>
  );
}
