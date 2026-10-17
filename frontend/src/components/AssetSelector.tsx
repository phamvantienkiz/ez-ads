'use client';

import React from 'react';
import { AdAccount, FacebookPage } from '@/types';
import { Layers, Flag, RefreshCw, AlertCircle } from 'lucide-react';

interface AssetSelectorProps {
  activeTab: 'dashboard' | 'create' | 'campaigns';
  onTabChange: (tab: 'dashboard' | 'create' | 'campaigns') => void;
  adAccounts: AdAccount[];
  selectedAccountId: string;
  onSelectAccount: (accountId: string) => void;
  pages: FacebookPage[];
  selectedPageId: string;
  onSelectPage: (pageId: string) => void;
  connected: boolean;
  isLoadingAssets: boolean;
  onRefreshAssets: () => void;
}

export function AssetSelector({
  activeTab,
  onTabChange,
  adAccounts,
  selectedAccountId,
  onSelectAccount,
  pages,
  selectedPageId,
  onSelectPage,
  connected,
  isLoadingAssets,
  onRefreshAssets,
}: AssetSelectorProps) {
  const tabs = [
    { id: 'dashboard', label: 'Tổng quan' },
    { id: 'create', label: 'Tạo quảng cáo' },
    { id: 'campaigns', label: 'Chiến dịch' },
  ] as const;

  return (
    <div className="bg-white rounded-card border border-border-card p-4 sm:p-5 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-4">
      {/* Segmented Control Tabs */}
      <div className="bg-subtle rounded-2xl p-1 inline-flex border border-border-hairline self-start sm:self-auto">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`px-4 py-2 rounded-xl text-[13px] font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-white text-primary shadow-control'
                  : 'text-muted hover:text-primary'
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Asset Selectors Dropdowns */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        {/* Ad Account Dropdown */}
        <div className="flex items-center gap-2 bg-subtle px-3 py-1.5 rounded-xl border border-border-hairline">
          <Layers className="w-4 h-4 text-muted shrink-0" />
          <div className="flex flex-col">
            <span className="text-[10px] text-muted-soft uppercase font-semibold tracking-wider">
              Tài khoản Ads
            </span>
            <select
              value={selectedAccountId}
              onChange={(e) => onSelectAccount(e.target.value)}
              disabled={!connected || adAccounts.length === 0}
              className="bg-transparent text-[13px] font-medium text-primary focus:outline-none cursor-pointer disabled:cursor-not-allowed max-w-[210px] truncate"
            >
              {!connected ? (
                <option value="">Chưa kết nối Meta</option>
              ) : adAccounts.length === 0 ? (
                <option value="">Không có tài khoản</option>
              ) : (
                adAccounts.map((acc) => (
                  <option key={acc.id} value={acc.id}>
                    {acc.name} ({acc.currency})
                  </option>
                ))
              )}
            </select>
          </div>
        </div>

        {/* Facebook Page Dropdown */}
        <div className="flex items-center gap-2 bg-subtle px-3 py-1.5 rounded-xl border border-border-hairline">
          <Flag className="w-4 h-4 text-muted shrink-0" />
          <div className="flex flex-col">
            <span className="text-[10px] text-muted-soft uppercase font-semibold tracking-wider">
              Fanpage đại diện
            </span>
            <select
              value={selectedPageId}
              onChange={(e) => onSelectPage(e.target.value)}
              disabled={!connected || pages.length === 0}
              className="bg-transparent text-[13px] font-medium text-primary focus:outline-none cursor-pointer disabled:cursor-not-allowed max-w-[210px] truncate"
            >
              {!connected ? (
                <option value="">Chưa kết nối Meta</option>
              ) : pages.length === 0 ? (
                <option value="">Không có Fanpage</option>
              ) : (
                pages.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))
              )}
            </select>
          </div>
        </div>

        {/* Refresh Assets Button */}
        {connected && (
          <button
            onClick={onRefreshAssets}
            disabled={isLoadingAssets}
            title="Tải lại danh sách Ad Account và Page"
            className="w-10 h-10 rounded-xl bg-subtle hover:bg-[#ECECEF] text-muted hover:text-primary flex items-center justify-center transition-colors border border-border-hairline shrink-0"
          >
            <RefreshCw className={`w-4 h-4 ${isLoadingAssets ? 'animate-spin' : ''}`} />
          </button>
        )}
      </div>
    </div>
  );
}
