'use client';

import React from 'react';
import { ShieldCheck, Wifi, WifiOff, LogOut, Loader2 } from 'lucide-react';

interface HeaderProps {
  connected: boolean;
  isBackendHealthy: boolean;
  isLoading: boolean;
  onConnect: () => void;
  onDisconnect: () => void;
}

export function Header({
  connected,
  isBackendHealthy,
  isLoading,
  onConnect,
  onDisconnect,
}: HeaderProps) {
  return (
    <header className="bg-white rounded-card border border-border-card px-6 py-4 shadow-card flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      {/* Brand & Identity */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-ink flex items-center justify-center text-white font-bold text-lg shadow-sm">
          B
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-[17px] font-semibold text-primary tracking-tight">
              BAHA Ads Manager
            </h1>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-subtle text-muted border border-border-hairline">
              Meta API v20.0
            </span>
          </div>
          <p className="text-[12px] text-muted">
            Hệ thống tạo & quản trị quảng cáo sản phẩm tự động
          </p>
        </div>
      </div>

      {/* Status Badges & Action */}
      <div className="flex items-center gap-3 flex-wrap">
        {/* Backend Health Badge */}
        <div
          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[12px] font-medium border ${
            isBackendHealthy
              ? 'bg-[#EBF8F0] text-[#1FA63A] border-[#D1F2DD]'
              : 'bg-[#FFF0F2] text-[#E5483D] border-[#FDD0D5]'
          }`}
          title={isBackendHealthy ? 'Backend FastAPI đang hoạt động' : 'Không thể kết nối FastAPI (:8000)'}
        >
          {isBackendHealthy ? (
            <>
              <span className="w-1.5 h-1.5 rounded-full bg-[#1FA63A] animate-pulse" />
              <span>FastAPI Ready</span>
            </>
          ) : (
            <>
              <WifiOff className="w-3.5 h-3.5 text-[#E5483D]" />
              <span>Backend Offline</span>
            </>
          )}
        </div>

        {/* Meta Connection Controls */}
        {connected ? (
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-[12px] font-medium bg-[#D8F3E4] text-[#1FA63A] border border-[#BBEBD0]">
              <span className="w-1.5 h-1.5 rounded-full bg-[#1FA63A]" />
              Đã kết nối Meta
            </span>

            <button
              onClick={onDisconnect}
              disabled={isLoading}
              className="text-[12px] text-muted hover:text-data-alert hover:bg-subtle px-2.5 py-1.5 rounded-lg transition-colors flex items-center gap-1"
              title="Ngắt kết nối phiên Meta"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Ngắt kết nối</span>
            </button>
          </div>
        ) : (
          <button
            onClick={onConnect}
            disabled={isLoading || !isBackendHealthy}
            className="bg-[#1F5FFF] hover:bg-[#1850DE] text-white text-[13px] font-medium px-4 py-2 rounded-full shadow-control flex items-center gap-2 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
            )}
            <span>Connect Facebook</span>
          </button>
        )}
      </div>
    </header>
  );
}
