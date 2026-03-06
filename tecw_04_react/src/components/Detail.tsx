import type { ReactNode } from 'react'
import { Link } from '@tanstack/react-router'
import { ChevronLeft } from 'lucide-react'
import { cn } from '@/lib/utils'

// ── Back link ────────────────────────────────────────────────────────────────

export function BackLink({ to, label }: { to: string; label: string }) {
  return (
    <Link
      to={to}
      className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
    >
      <ChevronLeft className="h-4 w-4" />
      {label}
    </Link>
  )
}

// ── Info card with fields grid ───────────────────────────────────────────────

export function InfoCard({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <dl className={cn('grid grid-cols-2 gap-x-6 gap-y-4 rounded-lg border p-5 md:grid-cols-4', className)}>
      {children}
    </dl>
  )
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</dt>
      <dd className="mt-1 text-sm">{children}</dd>
    </div>
  )
}

// ── Section heading ───────────────────────────────────────────────────────────

export function SectionTitle({ children }: { children: ReactNode }) {
  return <h2 className="text-lg font-semibold">{children}</h2>
}

// ── Asset preview ─────────────────────────────────────────────────────────────

const IMG_EXT = /\.(jpe?g|png|gif|webp|avif|svg)(\?.*)?$/i

export function AssetPreview({ url }: { url: string }) {
  return IMG_EXT.test(url) ? (
    <img src={url} alt="" className="max-h-60 rounded-md border object-cover" />
  ) : (
    <a href={url} target="_blank" rel="noreferrer" className="break-all text-sm underline">
      {url}
    </a>
  )
}
