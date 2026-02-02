import type { Metadata } from "next";
import { SessionProvider } from "@/contexts/SessionContext";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI News Aggregation System",
  description: "Advanced AI-powered news aggregation with WebRAG technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
