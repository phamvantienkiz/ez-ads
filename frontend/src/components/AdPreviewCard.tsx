'use client';

import React, { useState } from 'react';
import { Eye, ExternalLink, Image as ImageIcon } from 'lucide-react';

interface AdPreviewCardProps {
  pageName: string;
  primaryText: string;
  headline: string;
  destinationUrl: string;
  imageUrl: string;
}

export function AdPreviewCard({
  pageName,
  primaryText,
  headline,
  destinationUrl,
  imageUrl,
}: AdPreviewCardProps) {
  const [imageError, setImageError] = useState(false);

  // Extract clean domain from destinationUrl
  let domain = 'baha.vn';
  try {
    if (destinationUrl) {
      const parsed = new URL(destinationUrl.startsWith('http') ? destinationUrl : `https://${destinationUrl}`);
      domain = parsed.hostname.replace('www.', '');
    }
  } catch {
    domain = 'baha.vn';
  }

  const initial = pageName ? pageName.trim().charAt(0).toUpperCase() : 'B';

  return (
    <div className="bg-subtle rounded-2xl p-5 border border-border-hairline flex flex-col gap-3.5 w-full">
      {/* Card Header Label */}
      <div className="flex items-center justify-between pb-1 border-b border-border-hairline">
        <div className="flex items-center gap-1.5 text-[12px] font-semibold text-muted uppercase tracking-wider">
          <Eye className="w-3.5 h-3.5 text-muted" />
          <span>Live Feed Preview (Mô phỏng Facebook)</span>
        </div>
        <span className="text-[11px] text-muted-soft">Single Image Link Ad</span>
      </div>

      {/* Simulated Facebook Post Header */}
      <div className="flex items-center gap-2.5">
        <div className="w-9 h-9 rounded-full bg-[#1F5FFF] text-white flex items-center justify-center text-[14px] font-semibold shadow-sm shrink-0">
          {initial}
        </div>
        <div className="flex flex-col min-w-0">
          <span className="text-[13px] font-semibold text-primary truncate leading-tight">
            {pageName || 'Tên Fanpage Facebook'}
          </span>
          <span className="text-[11px] text-muted-soft leading-tight mt-0.5">
            Được tài trợ · Sponsored · 🌐
          </span>
        </div>
      </div>

      {/* Primary Text */}
      <p className="text-[13px] text-primary leading-relaxed whitespace-pre-wrap break-words">
        {primaryText || 'Nội dung văn bản quảng cáo chính sẽ hiển thị tại đây...'}
      </p>

      {/* Image Preview Container (1.91:1 standard aspect ratio for Meta Link Ads) */}
      <div className="w-full aspect-[1.91/1] bg-white rounded-xl overflow-hidden border border-border-hairline relative flex items-center justify-center">
        {imageUrl && !imageError ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={imageUrl}
            alt="Ad creative preview"
            onError={() => setImageError(true)}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center text-muted-soft text-[12px] gap-1.5 bg-[#FAF9FB]">
            <ImageIcon className="w-7 h-7 text-muted-soft" />
            <span>{imageError ? 'Không thể tải ảnh từ URL' : 'Xem trước hình ảnh quảng cáo'}</span>
          </div>
        )}
      </div>

      {/* Link Bar & CTA */}
      <div className="bg-white rounded-xl p-3 border border-border-card shadow-sm flex items-center justify-between gap-3">
        <div className="flex flex-col min-w-0">
          <span className="text-[11px] text-muted uppercase tracking-wider truncate">
            {domain}
          </span>
          <span className="text-[13px] font-semibold text-primary truncate">
            {headline || 'Tiêu đề bài viết quảng cáo'}
          </span>
          <span className="text-[11px] text-muted-soft truncate">
            Nhấn vào đây để xem chi tiết ưu đãi sản phẩm.
          </span>
        </div>

        <div className="shrink-0">
          <span className="inline-flex items-center px-3 py-1.5 rounded-lg bg-subtle border border-border-card text-[12px] font-medium text-primary shadow-control">
            Tìm hiểu thêm
          </span>
        </div>
      </div>
    </div>
  );
}
