import type { Metadata } from 'next'
import './globals.css'
import { Toaster } from 'react-hot-toast'

export const metadata: Metadata = {
  title: 'BMAD UI - Enhanced Agent Methodology Interface',
  description: 'A cosmic-themed, user-friendly frontend for the BMAD agent methodology with real-time workflow execution and stunning visual effects',
  keywords: 'BMAD, agents, methodology, development, workflow, cosmic, UI',
  authors: [{ name: 'Gil Alexander', url: 'https://github.com/gilalexander1' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#00ff41',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link 
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" 
          rel="stylesheet" 
        />
      </head>
      <body className="min-h-screen">
        <div className="relative min-h-screen">
          {/* Cosmic background effects */}
          <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
            <div className="absolute inset-0 bg-gradient-to-br from-cosmic-900 via-cosmic-800 to-matrix-dark" />
            <div className="absolute top-10 left-10 w-32 h-32 bg-cosmic-500/20 rounded-full blur-xl animate-pulse" />
            <div className="absolute top-40 right-20 w-24 h-24 bg-matrix-green/30 rounded-full blur-lg animate-float" />
            <div className="absolute bottom-20 left-20 w-40 h-40 bg-cosmic-400/10 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }} />
            <div className="absolute bottom-40 right-40 w-20 h-20 bg-cosmic-accent/20 rounded-full blur-lg animate-float" style={{ animationDelay: '2s' }} />
          </div>
          
          {/* Main content */}
          <main className="relative z-10">
            {children}
          </main>
        </div>
        
        {/* Toast notifications with cosmic theme */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(0, 0, 0, 0.9)',
              color: '#00ff41',
              border: '1px solid rgba(0, 255, 65, 0.3)',
              borderRadius: '12px',
              backdropFilter: 'blur(10px)',
              fontFamily: 'JetBrains Mono, monospace',
            },
            success: {
              iconTheme: {
                primary: '#00ff41',
                secondary: '#000000',
              },
            },
            error: {
              iconTheme: {
                primary: '#ff0066',
                secondary: '#000000',
              },
            },
          }}
        />
      </body>
    </html>
  )
}