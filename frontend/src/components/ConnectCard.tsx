'use client';

import React, { useState, useEffect } from 'react';
import { KeyRound, CheckCircle2, ShieldAlert, ArrowRight, Loader2, ChevronDown, ChevronUp } from 'lucide-react';

interface ConnectCardProps {
  connected: boolean;
  isLoading: boolean;
  updatedAt?: string;
  currentAppId?: string | null;
  onConnect: (appId?: string) => void;
  onDirectTokenSubmit?: (token: string) => void;
  onSelectTab: (tab: 'dashboard' | 'create' | 'campaigns') => void;
}

export function ConnectCard({
  connected,
  isLoading,
  updatedAt,
  currentAppId,
  onConnect,
  onDirectTokenSubmit,
  onSelectTab,
}: ConnectCardProps) {
  const [appIdInput, setAppIdInput] = useState<string>('');
  const [showDirectToken, setShowDirectToken] = useState<boolean>(false);
  const [directTokenInput, setDirectTokenInput] = useState<string>('');

  useEffect(() => {
    if (currentAppId) {
      setAppIdInput(currentAppId);
    } else if (typeof window !== 'undefined') {
      const saved = window.localStorage.getItem('baha_meta_app_id');
      if (saved) setAppIdInput(saved);
    }
  }, [currentAppId]);

  const handleConnectClick = () => {
    const trimmed = appIdInput.trim();
    if (trimmed && typeof window !== 'undefined') {
      window.localStorage.setItem('baha_meta_app_id', trimmed);
    }
    onConnect(trimmed || undefined);
  };

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
    <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col gap-4">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#D9E8FF] border border-[#C2DBFE] flex items-center justify-center text-[#1F5FFF] shrink-0">
            <KeyRound className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-[17px] font-semibold text-primary">
                Kết nối tài khoản Meta / Facebook (OAuth Implicit Flow)
              </h2>
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-[#EBF8F0] text-[#1FA63A]">
                Không cần App Secret
              </span>
            </div>
            <p className="text-[13px] text-muted mt-1 max-w-2xl">
              Nhập <strong>ID ứng dụng (Meta App ID)</strong> của tài khoản BAHA rồi bấm <strong>Connect Facebook ngay</strong>. Hệ thống sử dụng cơ chế <code className="text-primary font-mono text-[12px] bg-subtle px-1 rounded">response_type=token</code> nên không yêu cầu khóa bí mật (App Secret).
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 shrink-0">
          <input
            type="text"
            value={appIdInput}
            onChange={(e) => setAppIdInput(e.target.value)}
            placeholder="Nhập Meta App ID (VD: 123456789012345)"
            className="bg-subtle hover:bg-[#ECECEF] focus:bg-white text-primary text-[13px] font-mono rounded-xl px-3.5 py-2.5 border border-border-card focus:outline-none w-full sm:w-64"
          />
          <button
            onClick={handleConnectClick}
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
      </div>

      <div className="pt-3 border-t border-border-hairline flex flex-col gap-3">
        <div className="flex flex-wrap items-center justify-between gap-2 text-[12px] text-muted">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-[#FF8A1F] shrink-0" />
            <span>
              Lưu ý trên Meta App: Tại <strong>Facebook Login &gt; Settings</strong>, đảm bảo bật <em>Client OAuth Login</em> và thêm <code className="font-mono bg-subtle px-1 rounded text-primary">http://localhost:8000/api/meta/callback</code> vào <em>Valid OAuth Redirect URIs</em>.
            </span>
          </div>
          {onDirectTokenSubmit && (
            <button
              type="button"
              onClick={() => setShowDirectToken(!showDirectToken)}
              className="text-[#1F5FFF] hover:underline font-medium flex items-center gap-1 shrink-0"
            >
              <span>{showDirectToken ? 'Ẩn nhập Token trực tiếp' : 'Hoặc dán trực tiếp Access Token'}</span>
              {showDirectToken ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>

        {showDirectToken && onDirectTokenSubmit && (
          <div className="bg-subtle p-3.5 rounded-xl border border-border-hairline flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
            <input
              type="password"
              value={directTokenInput}
              onChange={(e) => setDirectTokenInput(e.target.value)}
              placeholder="Dán mã EAAB... từ Graph API Explorer (nếu chưa cấu hình Redirect URI)"
              className="flex-1 bg-white text-primary text-[13px] font-mono rounded-xl px-3.5 py-2 border border-border-card focus:outline-none"
            />
            <button
              type="button"
              disabled={!directTokenInput.trim() || isLoading}
              onClick={() => {
                if (directTokenInput.trim()) {
                  onDirectTokenSubmit(directTokenInput.trim());
                  setDirectTokenInput('');
                }
              }}
              className="bg-ink hover:bg-black text-white text-[13px] font-medium px-4 py-2 rounded-xl disabled:opacity-50 shrink-0"
            >
              Lưu Token & Kết nối
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
