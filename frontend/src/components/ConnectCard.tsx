'use client';

import React from 'react';
import { KeyRound, CheckCircle2, ShieldAlert, ArrowRight, Loader2 } from 'lucide-react';

interface ConnectCardProps {
  connected: boolean;
  isLoading: boolean;
  updatedAt?: string;
  onConnect: () => void;
  onSelectTab: (tab: 'dashboard' | 'create' | 'campaigns') => void;
}

export function ConnectCard({
  connected,
  isLoading,
  updatedAt,
  onConnect,
  onSelectTab,
}: ConnectCardProps) {
  if (connected) {
    return (
      <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#EBF8F0] border border-[#D1F2DD] flex items-center justify-center text-[#1FA63A] shrink-0">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-[17px] font-semibold text-primary">
              Phiên kết nối Meta Marketing API đang hoạt động
            </h2>
            <p className="text-[13px] text-muted mt-0.5">
              Token truy cập đã được lưu trữ an toàn trong cơ sở dữ liệu SQLite cục bộ (bảng <code className="text-primary font-mono text-[12px] bg-subtle px-1.5 py-0.5 rounded">meta_sessions</code>).
            </p>
            {updatedAt && (
              <p className="text-[11px] text-muted-soft mt-1">
                Lần cập nhật gần nhất: {new Date(updatedAt).toLocaleString('vi-VN')}
              </p>
            )}
          </div>
        </div>

        <button
          onClick={() => onSelectTab('create')}
          className="bg-ink hover:bg-black text-white text-[13px] font-medium px-4 py-2.5 rounded-xl shadow-primary flex items-center justify-center gap-2 transition-all active:scale-[0.98] shrink-0"
        >
          <span>Tạo chiến dịch mới</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-card border border-border-card p-6 shadow-card">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#D9E8FF] border border-[#C2DBFE] flex items-center justify-center text-[#1F5FFF] shrink-0">
            <KeyRound className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-[17px] font-semibold text-primary">
                Chưa kết nối tài khoản Meta / Facebook
              </h2>
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-[#FFF1C9] text-[#FF8A1F]">
                Cần thiết
              </span>
            </div>
            <p className="text-[13px] text-muted mt-1 max-w-2xl">
              Vui lòng kết nối tài khoản Facebook để cấp quyền truy cập tài khoản quảng cáo (<code className="text-primary font-mono text-[12px] bg-subtle px-1 rounded">ads_management</code>) và Fanpage (<code className="text-primary font-mono text-[12px] bg-subtle px-1 rounded">pages_manage_ads</code>) trước khi tạo chiến dịch.
            </p>
          </div>
        </div>

        <button
          onClick={onConnect}
          disabled={isLoading}
          className="bg-[#1F5FFF] hover:bg-[#1850DE] text-white text-[14px] font-medium px-5 py-2.5 rounded-xl shadow-control flex items-center justify-center gap-2 transition-all active:scale-[0.98] disabled:opacity-50 shrink-0"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
            </svg>
          )}
          <span>Connect Facebook ngay</span>
        </button>
      </div>

      <div className="mt-4 pt-4 border-t border-border-hairline flex items-center gap-2 text-[12px] text-muted">
        <ShieldAlert className="w-4 h-4 text-[#FF8A1F] shrink-0" />
        <span>Bảo mật: Mã App Secret và Access Token chỉ lưu tại Backend uvicorn / SQLite cục bộ, không bao giờ lộ ra trình duyệt.</span>
      </div>
    </div>
  );
}
