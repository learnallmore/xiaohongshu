import type { Metadata } from "next";
import { DM_Sans, Noto_Sans_SC, Noto_Serif_SC } from "next/font/google";
import "./globals.css";

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-ui",
  display: "swap",
});

const notoSans = Noto_Sans_SC({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-note-sans",
  display: "swap",
});

const notoSerif = Noto_Serif_SC({
  subsets: ["latin"],
  weight: ["600", "700"],
  variable: "--font-note-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: "棱镜 · 笔记审阅",
  description: "小众审美生活方式账号运营台",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="zh-CN"
      className={`${dmSans.variable} ${notoSans.variable} ${notoSerif.variable}`}
    >
      <body style={{ fontFamily: "var(--font-ui), system-ui, sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
