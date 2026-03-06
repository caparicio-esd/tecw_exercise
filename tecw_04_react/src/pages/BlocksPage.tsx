import { useQuery } from '@tanstack/react-query'
import { Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { ChevronRight } from 'lucide-react'
import { api, type Block } from '@/lib/api'
import { DataTable } from '@/components/DataTable'
import { Badge } from '@/components/ui/badge'

const columns: ColumnDef<Block, unknown>[] = [
  { accessorKey: 'id',    header: 'ID',    cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  { accessorKey: 'name',  header: 'Name',  cell: i => <span className="font-medium">{i.getValue() as string}</span> },
  { accessorKey: 'grade', header: 'Grade', cell: i => <Badge variant="outline">{i.getValue() as string}</Badge> },
  {
    accessorKey: 'color', header: 'Color',
    cell: i => (
      <div className="flex items-center gap-2">
        <span className="h-4 w-4 rounded-full border" style={{ backgroundColor: i.getValue() as string }} />
        <code className="text-xs">{i.getValue() as string}</code>
      </div>
    ),
  },
  { accessorKey: 'sector', header: 'Sector' },
  { accessorKey: 'height', header: 'Height', cell: i => <>{i.getValue() as number} m</> },
  { accessorKey: 'city',   header: 'City',   cell: i => <span className="capitalize">{i.getValue() as string}</span> },
  {
    accessorKey: 'active', header: 'Status',
    cell: i => i.getValue() ? <Badge variant="success">Active</Badge> : <Badge variant="secondary">Inactive</Badge>,
  },
  {
    id: '_link', header: '',
    cell: i => (
      <Link to="/blocks/$blockId" params={{ blockId: String(i.row.original.id) }}
        className="flex justify-end text-muted-foreground hover:text-foreground">
        <ChevronRight className="h-4 w-4" />
      </Link>
    ),
  },
]

export function BlocksPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['blocks'], queryFn: api.blocks })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Blocks</h1>
        {data && <span className="text-sm text-muted-foreground">{data.pagination.total} total</span>}
      </div>
      <DataTable columns={columns} data={data?.data ?? []} isLoading={isLoading} error={error} />
    </div>
  )
}
