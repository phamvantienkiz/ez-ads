/**
 * Shared TypeScript interfaces for BAHA Ads Manager
 * Grounded on docs/implementation/release-1/api/v1.md
 */

export interface ApiResponse<T = any> {
  success: boolean;
  statusCode: number;
  message: string;
  data?: T;
  meta?: {
    timestamp?: string;
    requestId?: string;
    total?: number;
    count?: number;
    limit?: number;
    adAccountId?: string;
    [key: string]: any;
  };
  error?: {
    code: string;
    message?: string;
    details?: any;
    failedStep?: string;
  };
}

export interface MetaSessionStatus {
  connected: boolean;
  tokenType?: string;
  hasToken: boolean;
  updatedAt?: string;
}

export interface AdAccount {
  id: string;          // e.g. "act_1234567890"
  accountId: string;   // e.g. "1234567890"
  name: string;        // e.g. "BAHA Commerce Account"
  currency: string;    // e.g. "VND" or "USD"
  accountStatus: number;
}

export interface FacebookPage {
  id: string;          // e.g. "100200300400"
  name: string;        // e.g. "BAHA Fashion Store"
  category?: string;   // e.g. "Clothing Store"
}

export interface Campaign {
  id: string;          // e.g. "120210000000001"
  name: string;
  objective: string;   // e.g. "OUTCOME_TRAFFIC"
  status: string;      // e.g. "PAUSED", "ACTIVE"
  createdTime: string; // ISO 8601 string
}

export interface CreateAdPayload {
  adAccountId: string;
  pageId: string;
  campaignName: string;
  budgetAmount: number;
  primaryText: string;
  headline: string;
  destinationUrl: string;
  imageUrl: string;
  adsetName?: string;
  adName?: string;
}

export interface CreationResources {
  imageHash: string | null;
  campaignId: string | null;
  adsetId: string | null;
  creativeId: string | null;
  adId: string | null;
}

export interface AdCreationResult {
  runId: number;
  status: 'success' | 'partial_failure' | 'failed';
  adAccountId?: string;
  pageId?: string;
  resources?: CreationResources;
  createdResources?: CreationResources;
  configuration?: {
    objective?: string;
    status?: string;
    billingEvent?: string;
    optimizationGoal?: string;
    bidStrategy?: string;
    targeting?: {
      geoLocations?: { countries: string[] };
      ageMin?: number;
      ageMax?: number;
    };
    cta?: string;
  };
}

export interface AdRunHistory {
  id: number;
  status: string;
  adAccountId: string;
  pageId: string;
  campaignId: string | null;
  adsetId: string | null;
  creativeId: string | null;
  adId: string | null;
  errorMessage: string | null;
  createdAt: string;
}

export interface HealthCheck {
  status: string;
  version: string;
  database: string;
  environment: string;
}
