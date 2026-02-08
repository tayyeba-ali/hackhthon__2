import './globals.css'
import type { Metadata } from 'next'
import { Outfit } from 'next/font/google'
import { Providers } from '@/components/providers'
import Header from '@/components/layout/Header'
import PageTransition from '@/components/layout/PageTransition'

/**
 * T009: Configure Outfit font (Premium, Geometric)
 * All weights from 300-900 for modern typography
 */
const outfit = Outfit({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  display: 'swap',
  variable: '--font-outfit',
})

export const metadata: Metadata = {
  title: 'TaskNova - Professional Task Management',
  description: 'A stunning, professional-grade task management application with modern UI and powerful features',
}

/**
 * T014: Root layout wrapping children with ThemeProvider
 * ThemeProvider manages theme detection, persistence, and class toggling
 * T077: ToastProvider for toast notifications
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={outfit.className}>
        <Providers>
          <Header />
          <main>
            <PageTransition>
              {children}
            </PageTransition>
          </main>
        </Providers>
      </body>
    </html>
  )
}
