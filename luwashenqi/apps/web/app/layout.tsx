import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { QueryProvider } from '@/components/common/QueryProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'KidVenture — Bay Area Kid-Friendly Places by Age',
  description: 'Find the best kid-friendly places in the Bay Area, filtered by your child\'s age.',
  keywords: 'kids activities, Bay Area, family fun, playground, children museum, indoor play, San Francisco',
  openGraph: {
    title: 'KidVenture',
    description: 'Discover the best kid-friendly places in the Bay Area, matched to your child\'s age',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  )
}
