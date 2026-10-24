import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "한 줄 자기소개 다듬기",
  description: "자기소개 한 줄을 면접용 · SNS용 · 발표용으로 다듬어 줍니다",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
