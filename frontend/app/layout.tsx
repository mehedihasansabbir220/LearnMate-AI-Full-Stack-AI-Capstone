import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "LearnMate AI | Your personal study companion", description: "Turn topics and notes into a study guide, quiz, and revision plan." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
