import { Link } from '@tanstack/react-router'
import type { ReactNode } from 'react'

const NAV = [
  { to: '/ways',             label: 'Ways' },
  { to: '/blocks',           label: 'Blocks' },
  { to: '/places',           label: 'Places' },
  { to: '/users',            label: 'Users' },
  { to: '/activity-records', label: 'Activity' },
]

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        <div className="container flex h-14 items-center gap-8">
          <span className="font-bold tracking-tight">🧗 TecW</span>
          <nav className="flex items-center gap-1">
            {NAV.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className="rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground [&.active]:bg-accent [&.active]:text-accent-foreground [&.active]:font-medium"
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main className="container py-8">{children}</main>
    </div>
  )
}
