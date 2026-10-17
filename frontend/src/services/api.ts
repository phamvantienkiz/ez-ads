import {
  ApiResponse,
  HealthCheck,
  MetaSessionStatus,
  AdAccount,
  FacebookPage,
  Campaign,
  CreateAdPayload,
  AdCreationResult,
  AdRunHistory,
} from '@/types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

export class ApiError extends Error {
  statusCode: number;
  code?: string;
  failedStep?: string;
  data?: any;

  constructor(message: string, statusCode: number, code?: string, failedStep?: string, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.code = code;
    this.failedStep = failedStep;
    this.data = data;
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
  const url = `${BASE_URL}${API_PREFIX}${endpoint}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    const body: ApiResponse<T> = await res.json().catch(() => ({
      success: res.ok,
      statusCode: res.status,
      message: res.statusText || 'Lỗi xử lý phản hồi từ server',
    }));

    // If HTTP error or success === false
    if (!res.ok || !body.success) {
      const errorDetail = body.error;
      const message = errorDetail?.message || body.message || `Lỗi yêu cầu: ${res.status}`;
      throw new ApiError(
        message,
        res.status,
        errorDetail?.code,
        errorDetail?.failedStep,
        body.data
      );
    }

    return body;
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err;
    }
    // Network or parse error
    throw new ApiError(
      err?.message || 'Không thể kết nối đến máy chủ Backend FastAPI (:8000)',
      0,
      'NETWORK_ERROR'
    );
  }
}

export const api = {
  // 1. Health check
  getHealth: () => request<HealthCheck>('/health'),

  // 2. Meta OAuth
  getMetaConnectUrl: () => request<{ authUrl: string }>('/meta/connect'),
  getMetaStatus: () => request<MetaSessionStatus>('/meta/status'),
  disconnectMeta: () => request<{ connected: boolean }>('/meta/disconnect', { method: 'POST' }),

  // 3. Assets
  getAdAccounts: () => request<AdAccount[]>('/meta/ad-accounts'),
  getPages: () => request<FacebookPage[]>('/meta/pages'),

  // 4. Campaigns & Ads
  getCampaigns: (adAccountId: string) =>
    request<Campaign[]>(`/campaigns?ad_account_id=${encodeURIComponent(adAccountId)}`),

  createAd: (payload: CreateAdPayload) =>
    request<AdCreationResult>('/ads', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getLatestRun: () => request<AdRunHistory>('/ads/runs/latest'),
  getRunById: (runId: number | string) => request<AdRunHistory>(`/ads/runs/${runId}`),
};
