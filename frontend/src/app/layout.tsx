import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'BAHA Ads Manager — Meta Marketing Automation',
  description: 'Trình điều phối & Tạo quảng cáo Meta chính thức cho BAHA',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen antialiased selection:bg-[#1F5FFF]/10 selection:text-[#1F5FFF]">
        {children}
      </body>
    </html>
  );
}
