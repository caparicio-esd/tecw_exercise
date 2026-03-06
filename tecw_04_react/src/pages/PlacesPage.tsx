import { useQuery } from '@tanstack/react-query'
import { Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { ChevronRight } from 'lucide-react'
import { api, type Place } from '@/lib/api'
import { DataTable } from '@/components/DataTable'

const columns: ColumnDef<Place, unknown>[] = [
  { accessorKey: 'id',   header: 'ID',   cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  { accessorKey: 'name', header: 'Name', cell: i => <span className="font-medium">{i.getValue() as string}</span> },
  {
    accessorKey: 'description', header: 'Description',
    cell: i => <span className="text-muted-foreground text-sm">{(i.getValue() as string | undefined) ?? '—'}</span>,
  },
  {
    id: '_link', header: '',
    cell: i => (
      <Link to="/places/$placeId" params={{ placeId: String(i.row.original.id) }}
        className="flex justify-end text-muted-foreground hover:text-foreground">
        <ChevronRight className="h-4 w-4" />
      </Link>
    ),
  },
]

export function PlacesPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['places'], queryFn: api.places })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Places</h1>
        {data && <span className="text-sm text-muted-foreground">{data.pagination.total} total</span>}
      </div>
      <DataTable columns={columns} data={data?.data ?? []} isLoading={isLoading} error={error} />
    </div>
  )
}
