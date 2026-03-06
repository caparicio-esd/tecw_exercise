import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { api, type ActivityRecordForUser } from '@/lib/api'
import { Badge } from '@/components/ui/badge'
import { DataTable } from '@/components/DataTable'
import { BackLink, InfoCard, Field, SectionTitle, AssetPreview } from '@/components/Detail'

const arColumns: ColumnDef<ActivityRecordForUser, unknown>[] = [
  { accessorKey: 'id',   header: 'ID',   cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  { accessorKey: 'date', header: 'Date', cell: i => <span className="font-mono text-sm">{i.getValue() as string}</span> },
  {
    id: 'route', header: 'Way / Block',
    cell: i => {
      const { way, block } = i.row.original
      if (way)
        return <Link to="/ways/$wayId" params={{ wayId: String(way.id) }} className="flex items-center gap-1.5 hover:underline">
          <Badge variant="outline">{way.grade}</Badge><span className="text-sm">{way.name}</span>
        </Link>
      if (block)
        return <Link to="/blocks/$blockId" params={{ blockId: String(block.id) }} className="flex items-center gap-1.5 hover:underline">
          <Badge variant="outline">{block.grade}</Badge><span className="text-sm">{block.name}</span>
        </Link>
      return <span className="text-muted-foreground">—</span>
    },
  },
  {
    id: 'discipline', header: 'Discipline',
    cell: i => {
      const { way, block } = i.row.original
      if (way)   return <Badge variant="secondary">{way.type}</Badge>
      if (block) return <Badge variant="secondary">boulder</Badge>
      return null
    },
  },
  { accessorKey: 'notes', header: 'Notes', cell: i => <span className="text-xs text-muted-foreground">{(i.getValue() as string | undefined) ?? '—'}</span> },
]

export function UserDetailPage() {
  const { userId } = useParams({ from: '/users/$userId' })
  const { data, isLoading, error } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => api.userById(Number(userId)),
  })

  if (isLoading) return <div className="flex h-48 items-center justify-center text-muted-foreground text-sm">Loading…</div>
  if (error || !data) return <div className="flex h-48 items-center justify-center text-destructive text-sm">{String(error)}</div>

  return (
    <div className="space-y-6">
      <BackLink to="/users" label="Users" />

      <div className="flex flex-wrap items-center gap-3">
        <span className="text-4xl">{data.avatar}</span>
        <h1 className="text-3xl font-bold">{data.name}</h1>
        {data.role === 'admin'
          ? <Badge>admin</Badge>
          : <Badge variant="secondary">user</Badge>}
        {data.active ? <Badge variant="success">Active</Badge> : <Badge variant="secondary">Inactive</Badge>}
      </div>

      <InfoCard>
        <Field label="Email">{data.email}</Field>
        <Field label="Member since">{data.memberSince}</Field>
        <Field label="Level"><span className="font-mono">{data.level}</span></Field>
        <Field label="Sessions"><span className="font-mono">{data.sessions}</span></Field>
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
