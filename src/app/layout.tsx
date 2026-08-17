import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "M. Wildan Nuril Akmal | Data Analyst • Power BI • ML Engineer",
  description: "Data Analyst & Machine Learning Engineer specializing in Power BI dashboards, ETL pipelines, and predictive modeling. Mathematics graduate with 1+ years of experience.",
  keywords: ["Data Analyst", "Power BI", "Machine Learning", "Business Intelligence", "Python", "BigQuery", "DAX", "ETL", "Portfolio"],
  authors: [{ name: "M. Wildan Nuril Akmal" }],
  openGraph: {
    title: "M. Wildan Nuril Akmal | Data Analyst • Power BI • ML Engineer",
    description: "Data Analyst & Machine Learning Engineer specializing in Power BI dashboards, ETL pipelines, and predictive modeling. Mathematics graduate with 1+ years of experience.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
