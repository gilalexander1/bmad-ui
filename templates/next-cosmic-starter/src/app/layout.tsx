export const metadata = { title: 'Cosmic Starter', description: 'BMAD Cosmic UI starter' }

import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen relative cosmic-bg cosmic-stars">
        {children}
      </body>
    </html>
  )
}

