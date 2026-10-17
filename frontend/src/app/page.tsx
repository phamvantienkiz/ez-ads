'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { api, ApiError } from '@/services/api';
import {
  MetaSessionStatus,
  AdAccount,
  FacebookPage,
  Campaign,
  CreateAdPayload,
  AdCreationResult,
  AdRunHistory,
} from '@/types';
import { Header } from '@/components/Header';
import { AssetSelector } from '@/components/AssetSelector';
import { ConnectCard } from '@/components/ConnectCard';
import { AdForm } from '@/components/AdForm';
import { AdPreviewCard } from '@/components/AdPreviewCard';
import { ResultPanel } from '@/components/ResultPanel';
import { CampaignTable } from '@/components/CampaignTable';
import {
  TrendingUp,
  FolderKanban,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  ExternalLink,
  ShieldCheck,
  Clock,
  Layers,
} from 'lucide-react';

export default function Home() {
  // Navigation State
  const [activeTab, setActiveTab] = useState<'dashboard' | 'create' | 'campaigns'>('dashboard');

  // Backend & Meta Status
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(true);
  const [metaStatus, setMetaStatus] = useState<MetaSessionStatus>({
    connected: false,
    hasToken: false,
  });

  // Assets State
  const [adAccounts, setAdAccounts] = useState<AdAccount[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string>('');
  const [pages, setPages] = useState<FacebookPage[]>([]);
  const [selectedPageId, setSelectedPageId] = useState<string>('');

  // Campaigns & History State
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [latestRun, setLatestRun] = useState<AdRunHistory | null>(null);
  const [creationResult, setCreationResult] = useState<AdCreationResult | null>(null);

  // Form State
  const [formData, setFormData] = useState<CreateAdPayload>({
    adAccountId: '',
    pageId: '',
    campaignName: 'BAHA Polo Shirt Traffic Campaign',
    budgetAmount: 50000,
    primaryText: 'Trải nghiệm dòng áo Polo nam cao cấp từ BAHA với chất liệu thoáng mát vượt trội, độ bền cao và kiểu dáng hiện đại cho mọi dịp.',
    headline: 'Áo Polo Nam Cao Cấp BAHA — Ưu Đãi 20%',
    destinationUrl: 'https://baha.vn/products/polo-classic',
    imageUrl: 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800',
  });

  // Loading & Error States
  const [isLoadingAuth, setIsLoadingAuth] = useState(false);
  const [isLoadingAssets, setIsLoadingAssets] = useState(false);
  const [isLoadingCampaigns, setIsLoadingCampaigns] = useState(false);
  const [isSubmittingAd, setIsSubmittingAd] = useState(false);
  const [globalError, setGlobalError] = useState<string | null>(null);
  const [globalSuccess, setGlobalSuccess] = useState<string | null>(null);

  // Selected asset helpers
  const selectedAccount = adAccounts.find((a) => a.id === selectedAccountId);
  const selectedPage = pages.find((p) => p.id === selectedPageId);

  // 1. Initial Health Check & Session Status
  const checkHealthAndSession = useCallback(async () => {
    try {
      const healthRes = await api.getHealth();
      setIsBackendHealthy(healthRes.success && healthRes.data?.status === 'healthy');
    } catch {
      setIsBackendHealthy(false);
    }

    try {
      const statusRes = await api.getMetaStatus();
      if (statusRes.success && statusRes.data) {
        setMetaStatus(statusRes.data);
      }
    } catch {
      // If backend is not available, status remains disconnected
    }
  }, []);

  // 2. Fetch Assets (Ad Accounts & Pages)
  const fetchAssets = useCallback(async () => {
    if (!metaStatus.connected) return;

    setIsLoadingAssets(true);
    setGlobalError(null);

    try {
      const [accRes, pageRes] = await Promise.allSettled([
        api.getAdAccounts(),
        api.getPages(),
      ]);

      if (accRes.status === 'fulfilled' && accRes.value.success && accRes.value.data) {
        const accounts = accRes.value.data;
        setAdAccounts(accounts);
        if (accounts.length > 0 && !selectedAccountId) {
          setSelectedAccountId(accounts[0].id);
        }
      }

      if (pageRes.status === 'fulfilled' && pageRes.value.success && pageRes.value.data) {
        const pList = pageRes.value.data;
        setPages(pList);
        if (pList.length > 0 && !selectedPageId) {
          setSelectedPageId(pList[0].id);
        }
      }
    } catch (err: any) {
      setGlobalError(err?.message || 'Không thể tải danh sách tài sản từ Meta.');
    } finally {
      setIsLoadingAssets(false);
    }
  }, [metaStatus.connected, selectedAccountId, selectedPageId]);

  // 3. Fetch Campaigns for selected Ad Account
  const fetchCampaigns = useCallback(async () => {
    if (!selectedAccountId || !metaStatus.connected) return;

    setIsLoadingCampaigns(true);
    try {
      const res = await api.getCampaigns(selectedAccountId);
      if (res.success && res.data) {
        setCampaigns(res.data);
      }
    } catch (err: any) {
      // Non-blocking error for campaign list
    } finally {
      setIsLoadingCampaigns(false);
    }
  }, [selectedAccountId, metaStatus.connected]);

  // 4. Fetch Latest Ad Creation Run from SQLite
  const fetchLatestRun = useCallback(async () => {
    try {
      const res = await api.getLatestRun();
      if (res.success && res.data) {
        setLatestRun(res.data);
      }
    } catch {
      // Ignore if no runs exist yet
    }
  }, []);

  // On Mount: Parse URL params & load state
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('connected') === 'true') {
      setGlobalSuccess('Kết nối tài khoản Meta thành công!');
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (urlParams.get('error') === 'access_denied') {
      setGlobalError('Bạn đã hủy hoặc từ chối cấp quyền trên Facebook. Vui lòng thử lại.');
      window.history.replaceState({}, document.title, window.location.pathname);
    }

    checkHealthAndSession();
    fetchLatestRun();
  }, [checkHealthAndSession, fetchLatestRun]);

  // When connected status changes, load assets
  useEffect(() => {
    if (metaStatus.connected) {
      fetchAssets();
    }
  }, [metaStatus.connected, fetchAssets]);

  // When selected account changes, update form and fetch campaigns
  useEffect(() => {
    if (selectedAccountId) {
      setFormData((prev) => ({ ...prev, adAccountId: selectedAccountId }));
      fetchCampaigns();
    }
  }, [selectedAccountId, fetchCampaigns]);

  // When selected page changes, update form
  useEffect(() => {
    if (selectedPageId) {
      setFormData((prev) => ({ ...prev, pageId: selectedPageId }));
    }
  }, [selectedPageId]);

  // Handlers: OAuth Connect / Disconnect
  const handleConnectFacebook = async () => {
    setIsLoadingAuth(true);
    setGlobalError(null);
    try {
      const res = await api.getMetaConnectUrl();
      if (res.success && res.data?.authUrl) {
        window.location.href = res.data.authUrl;
      } else {
        setGlobalError('Không thể khởi tạo URL xác thực Meta.');
      }
    } catch (err: any) {
      setGlobalError(err?.message || 'Lỗi khi gọi API kết nối Meta.');
    } finally {
      setIsLoadingAuth(false);
    }
  };

  const handleDisconnect = async () => {
    if (!window.confirm('Bạn có chắc chắn muốn ngắt kết nối phiên làm việc Meta?')) return;
    setIsLoadingAuth(true);
    try {
      await api.disconnectMeta();
      setMetaStatus({ connected: false, hasToken: false });
      setAdAccounts([]);
      setSelectedAccountId('');
      setPages([]);
      setSelectedPageId('');
      setCampaigns([]);
      setGlobalSuccess('Đã ngắt kết nối phiên Meta thành công.');
    } catch (err: any) {
      setGlobalError(err?.message || 'Lỗi khi ngắt kết nối.');
    } finally {
      setIsLoadingAuth(false);
    }
  };

  // Handler: Ad Creation Submit
  const handleCreateAd = async (payload: CreateAdPayload) => {
    if (!selectedAccountId || !selectedPageId) {
      setGlobalError('Vui lòng chọn Tài khoản quảng cáo và Fanpage trước khi tạo.');
      return;
    }

    setIsSubmittingAd(true);
    setGlobalError(null);
    setGlobalSuccess(null);

    const submissionPayload: CreateAdPayload = {
      ...payload,
      adAccountId: selectedAccountId,
      pageId: selectedPageId,
    };

    try {
      const res = await api.createAd(submissionPayload);
      if (res.success && res.data) {
        setCreationResult(res.data);
        setGlobalSuccess('Tạo quảng cáo thành công trên Meta Marketing API!');
        fetchLatestRun();
        fetchCampaigns();
      }
    } catch (err: any) {
      if (err instanceof ApiError && err.code === 'PARTIAL_CREATION_FAILURE') {
        setCreationResult({
          runId: err.data?.runId || 0,
          status: 'partial_failure',
          createdResources: err.data?.createdResources,
        });
        setGlobalError(err.message);
      } else {
        setGlobalError(err?.message || 'Đã có lỗi xảy ra khi tạo quảng cáo.');
      }
    } finally {
      setIsSubmittingAd(false);
    }
  };

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto flex flex-col gap-6">
      {/* 1. Header Bar */}
      <Header
        connected={metaStatus.connected}
        isBackendHealthy={isBackendHealthy}
        isLoading={isLoadingAuth}
        onConnect={handleConnectFacebook}
        onDisconnect={handleDisconnect}
      />

      {/* Backend Offline Warning Banner */}
      {!isBackendHealthy && (
        <div className="bg-[#FFF0F2] border border-[#FDD0D5] text-[#E5483D] p-4 rounded-card flex items-start gap-3 shadow-sm">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="text-[13px]">
            <p className="font-semibold">Không thể kết nối tới Backend FastAPI (:8000)</p>
            <p className="mt-0.5 text-muted">
              Vui lòng đảm bảo server uvicorn backend đang chạy tại cổng 8000 (<code className="font-mono bg-white px-1.5 py-0.5 rounded text-primary">uvicorn app.main:app --port 8000</code>).
            </p>
          </div>
        </div>
      )}

      {/* Global Alerts (Success / Error) */}
      {globalSuccess && (
        <div className="bg-[#EBF8F0] border border-[#D1F2DD] text-[#1FA63A] px-4 py-3 rounded-2xl text-[13px] font-medium flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{globalSuccess}</span>
          </div>
          <button
            onClick={() => setGlobalSuccess(null)}
            className="text-[#1FA63A] hover:opacity-75 text-[12px] font-semibold"
          >
            Đóng
          </button>
        </div>
      )}

      {globalError && (
        <div className="bg-[#FFF0F2] border border-[#FDD0D5] text-[#E5483D] px-4 py-3 rounded-2xl text-[13px] font-medium flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{globalError}</span>
          </div>
          <button
            onClick={() => setGlobalError(null)}
            className="text-[#E5483D] hover:opacity-75 text-[12px] font-semibold"
          >
            Đóng
          </button>
        </div>
      )}

      {/* 2. Asset & Navigation Bar */}
      <AssetSelector
        activeTab={activeTab}
        onTabChange={setActiveTab}
        adAccounts={adAccounts}
        selectedAccountId={selectedAccountId}
        onSelectAccount={setSelectedAccountId}
        pages={pages}
        selectedPageId={selectedPageId}
        onSelectPage={setSelectedPageId}
        connected={metaStatus.connected}
        isLoadingAssets={isLoadingAssets}
        onRefreshAssets={fetchAssets}
      />

      {/* 3. Dynamic Viewport Based on Active Tab */}

      {/* TAB 1: DASHBOARD */}
      {activeTab === 'dashboard' && (
        <div className="flex flex-col gap-6">
          {/* Connect Banner if disconnected */}
          {!metaStatus.connected && (
            <ConnectCard
              connected={metaStatus.connected}
              isLoading={isLoadingAuth}
              onConnect={handleConnectFacebook}
              onSelectTab={setActiveTab}
            />
          )}

          {/* 3 Hero Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Metric 1: Connection Status */}
            <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col justify-between">
              <span className="text-[13px] text-muted">Trạng thái kết nối</span>
              <div className="my-3">
                {metaStatus.connected ? (
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-[#1FA63A] animate-pulse" />
                    <span className="text-[20px] font-semibold text-primary">Connected</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-[#6B6B76]" />
                    <span className="text-[20px] font-semibold text-muted">Chưa kết nối</span>
                  </div>
                )}
              </div>
              <span className="text-[12px] text-muted-soft truncate">
                {selectedAccount ? `${selectedAccount.name}` : 'Chưa chọn tài khoản'}
              </span>
            </div>

            {/* Metric 2: Campaigns Count */}
            <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col justify-between">
              <span className="text-[13px] text-muted">Chiến dịch trên Ad Account</span>
              <div className="my-2 flex items-baseline gap-2">
                <span className="text-[44px] font-normal tracking-tight text-primary tabular-nums leading-none">
                  {campaigns.length}
                </span>
                <span className="text-[13px] text-muted">chiến dịch</span>
              </div>
              <button
                onClick={() => setActiveTab('campaigns')}
                className="text-[12px] font-medium text-[#1F5FFF] hover:underline flex items-center gap-1 self-start"
              >
                <span>Xem danh sách chi tiết</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {/* Metric 3: Latest Creation Status */}
            <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col justify-between">
              <span className="text-[13px] text-muted">Lần tạo gần nhất</span>
              <div className="my-3">
                {latestRun ? (
                  <span
                    className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[12px] font-semibold ${
                      latestRun.status === 'success'
                        ? 'bg-[#D8F3E4] text-[#1FA63A]'
                        : 'bg-[#FFD9E8] text-[#E5483D]'
                    }`}
                  >
                    <span
                      className={`w-1.5 h-1.5 rounded-full ${
                        latestRun.status === 'success' ? 'bg-[#1FA63A]' : 'bg-[#E5483D]'
                      }`}
                    />
                    {latestRun.status === 'success' ? 'Thành công (PAUSED)' : 'Thất bại một phần'}
                  </span>
                ) : (
                  <span className="text-[14px] text-muted">Chưa có lượt chạy</span>
                )}
              </div>
              <span className="text-[12px] text-muted-soft">
                {latestRun ? `Run ID #${latestRun.id} · ${new Date(latestRun.createdAt).toLocaleTimeString('vi-VN')}` : 'Phiên làm việc mới'}
              </span>
            </div>
          </div>

          {/* Latest Run Details Card */}
          <div className="bg-white rounded-card border border-border-card p-6 shadow-card flex flex-col gap-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-hairline">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-muted" />
                <h3 className="text-[16px] font-semibold text-primary">
                  Chi tiết phiên tạo tài nguyên gần nhất
                </h3>
              </div>
              <span className="text-[12px] text-muted-soft">
                Bảng lưu trữ SQLite: <code className="font-mono bg-subtle px-1.5 py-0.5 rounded text-primary">ad_creation_runs</code>
              </span>
            </div>

            {latestRun ? (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-subtle p-3 rounded-xl border border-border-hairline">
                    <span className="text-[11px] font-semibold text-muted-soft block uppercase">Campaign ID</span>
                    <span className="text-[13px] font-mono font-medium text-primary truncate block mt-0.5 tabular-nums">
                      {latestRun.campaignId || '—'}
                    </span>
                  </div>
                  <div className="bg-subtle p-3 rounded-xl border border-border-hairline">
                    <span className="text-[11px] font-semibold text-muted-soft block uppercase">Ad Set ID</span>
                    <span className="text-[13px] font-mono font-medium text-primary truncate block mt-0.5 tabular-nums">
                      {latestRun.adsetId || '—'}
                    </span>
                  </div>
                  <div className="bg-subtle p-3 rounded-xl border border-border-hairline">
                    <span className="text-[11px] font-semibold text-muted-soft block uppercase">Creative ID</span>
                    <span className="text-[13px] font-mono font-medium text-primary truncate block mt-0.5 tabular-nums">
                      {latestRun.creativeId || '—'}
                    </span>
                  </div>
                  <div className="bg-subtle p-3 rounded-xl border border-border-hairline">
                    <span className="text-[11px] font-semibold text-muted-soft block uppercase">Ad ID</span>
                    <span className="text-[13px] font-mono font-medium text-primary truncate block mt-0.5 tabular-nums">
                      {latestRun.adId || '—'}
                    </span>
                  </div>
                </div>

                {latestRun.errorMessage && (
                  <div className="bg-[#FFF0F2] border border-[#FDD0D5] text-[#E5483D] p-3 rounded-xl text-[12px]">
                    <strong>Thông báo lỗi:</strong> {latestRun.errorMessage}
                  </div>
                )}
              </div>
            ) : (
              <div className="py-8 flex flex-col items-center justify-center text-center gap-2 text-muted">
                <p className="text-[14px]">Chưa có lượt tạo quảng cáo nào trong phiên này.</p>
                <button
                  onClick={() => setActiveTab('create')}
                  className="mt-1 bg-ink hover:bg-black text-white text-[13px] font-medium px-4 py-2 rounded-xl shadow-primary flex items-center gap-1.5 transition-all"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Tạo quảng cáo ngay</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: CREATE AD */}
      {activeTab === 'create' && (
        <div className="flex flex-col gap-6">
          {/* Result Panel if ad was just submitted */}
          {creationResult && (
            <ResultPanel
              result={creationResult}
              onViewCampaigns={() => setActiveTab('campaigns')}
              onCreateAnother={() => setCreationResult(null)}
            />
          )}

          {/* 2-Column Grid: Form (7 parts) + Live Preview (5 parts) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Left Column: Form */}
            <div className="lg:col-span-7 bg-white rounded-card border border-border-card p-6 shadow-card">
              <AdForm
                initialValues={formData}
                selectedAccount={selectedAccount}
                isSubmitting={isSubmittingAd}
                errorMessage={globalError}
                onChange={setFormData}
                onSubmit={handleCreateAd}
              />
            </div>

            {/* Right Column: Sticky Live Preview */}
            <div className="lg:col-span-5 lg:sticky lg:top-8 flex flex-col gap-4">
              <AdPreviewCard
                pageName={selectedPage?.name || 'BAHA Fashion Store'}
                primaryText={formData.primaryText}
                headline={formData.headline}
                destinationUrl={formData.destinationUrl}
                imageUrl={formData.imageUrl}
              />
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: CAMPAIGNS */}
      {activeTab === 'campaigns' && (
        <CampaignTable
          campaigns={campaigns}
          isLoading={isLoadingCampaigns}
          selectedAccountId={selectedAccountId}
          onRefresh={fetchCampaigns}
          onNavigateCreate={() => setActiveTab('create')}
        />
      )}

      {/* Footer Info */}
      <footer className="text-center py-4 text-[12px] text-muted-soft">
        BAHA Ads Manager · MVP Architecture Release 1 · Soft Clean Cards
      </footer>
    </main>
  );
}
