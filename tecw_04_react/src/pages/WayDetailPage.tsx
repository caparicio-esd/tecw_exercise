import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { api, type ActivityRecordForWay } from '@/lib/api'
import { Badge } from '@/components/ui/badge'
import { DataTable } from '@/components/DataTable'
import { BackLink, InfoCard, Field, SectionTitle, AssetPreview } from '@/components/Detail'

const arColumns: ColumnDef<ActivityRecordForWay, unknown>[] = [
  { accessorKey: 'id',   header: 'ID',   cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  { accessorKey: 'date', header: 'Date', cell: i => <span className="font-mono text-sm">{i.getValue() as string}</span> },
  {
    id: 'user', header: 'User',
    cell: i => {
      const u = i.row.original.user
      return u
        ? <Link to="/users/$userId" params={{ userId: String(u.id) }} className="flex items-center gap-1.5 hover:underline">
            <span>{u.avatar}</span><span>{u.name}</span>
          </Link>
        : <span className="text-muted-foreground">—</span>
    },
  },
  { accessorKey: 'notes', header: 'Notes', cell: i => <span className="text-xs text-muted-foreground">{(i.getValue() as string | undefined) ?? '—'}</span> },
]

export function WayDetailPage() {
  const { wayId } = useParams({ from: '/ways/$wayId' })
  const { data, isLoading, error } = useQuery({
    queryKey: ['ways', wayId],
    queryFn: () => api.wayById(Number(wayId)),
  })

  if (isLoading) return <div className="flex h-48 items-center justify-center text-muted-foreground text-sm">Loading…</div>
  if (error || !data) return <div className="flex h-48 items-center justify-center text-destructive text-sm">{String(error)}</div>

  return (
    <div className="space-y-6">
      <BackLink to="/ways" label="Ways" />

      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-3xl font-bold">{data.name}</h1>
        <Badge variant="outline">{data.grade}</Badge>
        <Badge variant="secondary">{data.type}</Badge>
        {data.active ? <Badge variant="success">Active</Badge> : <Badge variant="secondary">Inactive</Badge>}
      </div>

      <InfoCard>
        <Field label="Length">{data.length} m</Field>
        <Field label="City"><span className="capitalize">{data.city}</span></Field>
        <Field label="Grade">{data.grade}</Field>
        <Field label="Type"><span className="capitalize">{data.type}</span></Field>
        {data.description && <Field label="Description"><span className="col-span-4 text-muted-foreground">{data.description}</span></Field>}
      </InfoCard>

      {data.mainAsset && (
        <div className="space-y-2">
          <SectionTitle>Media</SectionTitle>
          <AssetPreview url={data.mainAsset.url} />
        </div>
      )}

      <div className="space-y-3">
        <SectionTitle>Activity Records ({data.activityRecords.length})</SectionTitle>
        <DataTable columns={arColumns} data={data.activityRecords} />
      </div>
    </div>
  )
}
