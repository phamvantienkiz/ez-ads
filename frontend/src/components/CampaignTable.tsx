'use client';

import React, { useState } from 'react';
import { Campaign } from '@/types';
import { RefreshCw, Copy, Check, FolderKanban, Plus, ExternalLink, Loader2 } from 'lucide-react';

interface CampaignTableProps {
  campaigns: Campaign[];
  isLoading: boolean;
  selectedAccountId: string;
  onRefresh: () => void;
  onNavigateCreate: () => void;
}

export function CampaignTable({
  campaigns,
  isLoading,
  selectedAccountId,
  onRefresh,
  onNavigateCreate,
}: CampaignTableProps) {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const copyToClipboard = (id: string) => {
    navigator.clipboard.writeText(id);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col gap-5">
      {/* Table Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-border-hairline">
        <div>
          <div className="flex items-center gap-2.5">
            <h2 className="text-[22px] font-semibold text-primary tracking-tight">
              Danh sách chiến dịch trên Meta
            </h2>
            <span className="text-[12px] font-semibold px-2.5 py-0.5 rounded-full bg-subtle text-muted">
              {campaigns.length} chiến dịch
            </span>
          </div>
          <p className="text-[13px] text-muted mt-0.5">
            Dữ liệu trực tiếp từ Meta Marketing API cho tài khoản <code className="text-primary font-mono text-[12px] bg-subtle px-1.5 py-0.5 rounded">{selectedAccountId || 'Chưa chọn'}</code>
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={onRefresh}
            disabled={isLoading || !selectedAccountId}
            title="Làm mới danh sách từ Meta"
            className="h-9 px-3 rounded-xl bg-subtle hover:bg-[#ECECEF] text-muted hover:text-primary flex items-center gap-2 text-[13px] font-medium transition-colors border border-border-hairline shadow-control disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Làm mới</span>
          </button>

          <button
            onClick={onNavigateCreate}
            className="h-9 px-3.5 rounded-xl bg-ink hover:bg-black text-white flex items-center gap-1.5 text-[13px] font-medium transition-all shadow-primary active:scale-[0.98]"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Tạo mới</span>
          </button>
        </div>
      </div>

      {/* Content Area */}
      {isLoading ? (
        <div className="py-16 flex flex-col items-center justify-center gap-3 text-muted">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="text-[13px]">Đang truy vấn danh sách chiến dịch từ Meta Marketing API...</span>
        </div>
      ) : campaigns.length === 0 ? (
        /* Empty State */
        <div className="py-16 flex flex-col items-center justify-center text-center gap-3 bg-subtle/50 rounded-2xl border border-dashed border-border-card p-8">
          <div className="w-12 h-12 rounded-2xl bg-white border border-border-card flex items-center justify-center text-muted shadow-sm">
            <FolderKanban className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-[16px] font-semibold text-primary">
              Chưa có chiến dịch nào trên tài khoản này
            </h3>
            <p className="text-[13px] text-muted mt-1 max-w-md">
              Tài khoản quảng cáo được chọn hiện chưa có chiến dịch nào, hoặc chưa được tạo thông qua API.
            </p>
          </div>
          <button
            onClick={onNavigateCreate}
            className="mt-2 bg-ink hover:bg-black text-white text-[13px] font-medium px-4 py-2 rounded-xl shadow-primary flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Tạo chiến dịch quảng cáo đầu tiên</span>
          </button>
        </div>
      ) : (
        /* Borderless Minimal Table */
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-border-hairline text-[11px] font-semibold text-muted uppercase tracking-wider">
                <th className="py-3 px-3">Tên chiến dịch</th>
                <th className="py-3 px-3">Campaign ID</th>
                <th className="py-3 px-3">Mục tiêu</th>
                <th className="py-3 px-3">Trạng thái</th>
                <th className="py-3 px-3 text-right">Ngày tạo</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-hairline text-[13px]">
              {campaigns.map((camp) => (
                <tr
                  key={camp.id}
                  className="hover:bg-subtle/60 transition-colors group"
                >
                  {/* Campaign Name */}
                  <td className="py-3.5 px-3">
                    <span className="font-medium text-primary block truncate max-w-[280px]">
                      {camp.name}
                    </span>
                  </td>

                  {/* Campaign ID with Copy */}
                  <td className="py-3.5 px-3">
                    <div className="flex items-center gap-1.5 font-mono text-[12px] text-muted group-hover:text-primary tabular-nums">
                      <span>{camp.id}</span>
                      <button
                        onClick={() => copyToClipboard(camp.id)}
                        title="Sao chép Campaign ID"
                        className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white rounded transition-opacity"
                      >
                        {copiedId === camp.id ? (
                          <Check className="w-3 h-3 text-[#1FA63A]" />
                        ) : (
                          <Copy className="w-3 h-3 text-muted" />
                        )}
                      </button>
                    </div>
                  </td>

                  {/* Objective */}
                  <td className="py-3.5 px-3">
                    <span className="text-[12px] font-medium text-muted bg-subtle px-2 py-0.5 rounded-md border border-border-hairline">
                      {camp.objective || 'OUTCOME_TRAFFIC'}
                    </span>
                  </td>

                  {/* Status Badge */}
                  <td className="py-3.5 px-3">
                    {camp.status === 'ACTIVE' ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#D8F3E4] text-[#1FA63A]">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#1FA63A]" />
                        ACTIVE
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#FFF1C9] text-[#FF8A1F]">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#FF8A1F]" />
                        PAUSED
                      </span>
                    )}
                  </td>

                  {/* Created Time */}
                  <td className="py-3.5 px-3 text-right text-[12px] text-muted-soft tabular-nums">
                    {camp.createdTime ? new Date(camp.createdTime).toLocaleDateString('vi-VN') : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
