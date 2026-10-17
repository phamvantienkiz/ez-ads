'use client';

import React, { useState } from 'react';
import { AdCreationResult, CreationResources } from '@/types';
import { CheckCircle2, AlertTriangle, Copy, Check, ExternalLink, ArrowRight } from 'lucide-react';

interface ResultPanelProps {
  result: AdCreationResult;
  onViewCampaigns: () => void;
  onCreateAnother: () => void;
}

export function ResultPanel({
  result,
  onViewCampaigns,
  onCreateAnother,
}: ResultPanelProps) {
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const isSuccess = result.status === 'success';
  const resources: CreationResources = result.resources || result.createdResources || {
    imageHash: null,
    campaignId: null,
    adsetId: null,
    creativeId: null,
    adId: null,
  };

  const copyToClipboard = (key: string, text: string | null) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const resourceItems = [
    { key: 'campaignId', label: 'Campaign ID', value: resources.campaignId },
    { key: 'adsetId', label: 'Ad Set ID', value: resources.adsetId },
    { key: 'creativeId', label: 'Creative ID', value: resources.creativeId },
    { key: 'adId', label: 'Ad ID', value: resources.adId },
    { key: 'imageHash', label: 'Image Hash', value: resources.imageHash },
  ];

  return (
    <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col gap-6">
      {/* Status Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-hairline">
        <div className="flex items-center gap-3">
          <div
            className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${
              isSuccess
                ? 'bg-[#EBF8F0] border border-[#D1F2DD] text-[#1FA63A]'
                : 'bg-[#FFF0F2] border border-[#FDD0D5] text-[#E5483D]'
            }`}
          >
            {isSuccess ? (
              <CheckCircle2 className="w-6 h-6" />
            ) : (
              <AlertTriangle className="w-6 h-6" />
            )}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-[18px] font-semibold text-primary">
                {isSuccess ? 'Tạo quảng cáo thành công trên Meta' : 'Thất bại một phần (Partial Failure)'}
              </h3>
              <span
                className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full ${
                  isSuccess
                    ? 'bg-[#D8F3E4] text-[#1FA63A]'
                    : 'bg-[#FFD9E8] text-[#E5483D]'
                }`}
              >
                {isSuccess ? 'RUN ID #' + result.runId : 'LỖI BƯỚC THAO TÁC'}
              </span>
            </div>
            <p className="text-[13px] text-muted mt-0.5">
              {isSuccess
                ? 'Tất cả 5 tài nguyên đã được tạo thật trên Meta Marketing API và mặc định ở trạng thái PAUSED.'
                : 'Một số tài nguyên ban đầu đã được tạo, nhưng bước tiếp theo gặp phản hồi lỗi từ Meta API.'}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={onCreateAnother}
            className="px-4 py-2 rounded-xl text-[13px] font-medium text-muted hover:text-primary bg-subtle hover:bg-[#ECECEF] transition-colors"
          >
            Tạo thêm bài mới
          </button>
          <button
            onClick={onViewCampaigns}
            className="bg-ink hover:bg-black text-white text-[13px] font-medium px-4 py-2 rounded-xl shadow-primary flex items-center gap-1.5 transition-all"
          >
            <span>Xem chiến dịch</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Grid of Real IDs */}
      <div>
        <h4 className="text-[12px] font-semibold text-muted uppercase tracking-wider mb-3">
          Tài nguyên thật đã ghi nhận (Meta Marketing API v20.0)
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {resourceItems.map((item) => (
            <div
              key={item.key}
              className={`p-3.5 rounded-xl border flex flex-col justify-between gap-1 transition-all ${
                item.value
                  ? 'bg-subtle border-border-hairline'
                  : 'bg-[#FFF9FA] border-dashed border-[#FDD0D5] opacity-60'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-muted-soft uppercase">
                  {item.label}
                </span>
                {item.value && (
                  <button
                    onClick={() => copyToClipboard(item.key, item.value)}
                    title="Sao chép ID"
                    className="text-muted hover:text-primary p-1 rounded hover:bg-white transition-colors"
                  >
                    {copiedKey === item.key ? (
                      <Check className="w-3.5 h-3.5 text-[#1FA63A]" />
                    ) : (
                      <Copy className="w-3.5 h-3.5" />
                    )}
                  </button>
                )}
              </div>
              <div className="text-[13px] font-mono text-primary font-medium truncate tabular-nums">
                {item.value || '(Chưa tạo)'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Configuration Summary Badge Row */}
      <div className="bg-subtle rounded-xl p-4 border border-border-hairline flex flex-wrap items-center justify-between gap-3 text-[12px]">
        <div className="flex items-center gap-2">
          <span className="text-muted">Mục tiêu:</span>
          <span className="font-semibold text-primary">OUTCOME_TRAFFIC</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-muted">Trạng thái:</span>
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#FFF1C9] text-[#FF8A1F] font-semibold text-[11px]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF8A1F]" />
            PAUSED
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-muted">Targeting:</span>
          <span className="font-medium text-primary">Việt Nam (18–65)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-muted">Tối ưu hóa:</span>
          <span className="font-medium text-primary">LINK_CLICKS</span>
        </div>
      </div>
    </div>
  );
}
