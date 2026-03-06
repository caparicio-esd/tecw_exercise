import { useQuery } from '@tanstack/react-query'
import { Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { ChevronRight } from 'lucide-react'
import { api, type ActivityRecord } from '@/lib/api'
import { DataTable } from '@/components/DataTable'
import { Badge } from '@/components/ui/badge'

const columns: ColumnDef<ActivityRecord, unknown>[] = [
  { accessorKey: 'id',   header: 'ID',   cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  { accessorKey: 'date', header: 'Date', cell: i => <span className="font-mono text-sm">{i.getValue() as string}</span> },
  {
    id: 'user', header: 'User',
    cell: i => {
      const u = i.row.original.user
      return u
        ? <Link to="/users/$userId" params={{ userId: String(u.id) }} className="flex items-center gap-1.5 hover:underline">
            <span>{u.avatar}</span><span className="text-sm">{u.name}</span>
          </Link>
        : <span className="text-muted-foreground">—</span>
    },
  },
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
  {
    accessorKey: 'notes', header: 'Notes',
    cell: i => <span className="max-w-xs truncate text-xs text-muted-foreground">{(i.getValue() as string | undefined) ?? '—'}</span>,
  },
  {
    id: '_link', header: '',
    cell: i => (
      <Link to="/activity-records/$recordId" params={{ recordId: String(i.row.original.id) }}
        className="flex justify-end text-muted-foreground hover:text-foreground">
        <ChevronRight className="h-4 w-4" />
      </Link>
    ),
  },
]

export function ActivityRecordsPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['activity-records'], queryFn: api.activityRecords })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Activity Records</h1>
        {data && <span className="text-sm text-muted-foreground">{data.pagination.total} total</span>}
      </div>
      <DataTable columns={columns} data={data?.data ?? []} isLoading={isLoading} error={error} />
    </div>
  )
}
