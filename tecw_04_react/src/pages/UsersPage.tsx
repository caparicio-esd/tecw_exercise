import { useQuery } from '@tanstack/react-query'
import { Link } from '@tanstack/react-router'
import type { ColumnDef } from '@tanstack/react-table'
import { ChevronRight } from 'lucide-react'
import { api, type User } from '@/lib/api'
import { DataTable } from '@/components/DataTable'
import { Badge } from '@/components/ui/badge'

const columns: ColumnDef<User, unknown>[] = [
  { accessorKey: 'id',   header: 'ID',   cell: i => <span className="text-muted-foreground">{i.getValue() as number}</span> },
  {
    accessorKey: 'name', header: 'Name',
    cell: i => (
      <div className="flex items-center gap-2">
        <span>{i.row.original.avatar}</span>
        <span className="font-medium">{i.getValue() as string}</span>
      </div>
    ),
  },
  { accessorKey: 'email',       header: 'Email',        cell: i => <span className="text-sm">{i.getValue() as string}</span> },
  {
    accessorKey: 'role', header: 'Role',
    cell: i => (i.getValue() as string) === 'admin' ? <Badge>admin</Badge> : <Badge variant="secondary">user</Badge>,
  },
  { accessorKey: 'level',       header: 'Level',    cell: i => <span className="font-mono">{i.getValue() as number}</span> },
  { accessorKey: 'sessions',    header: 'Sessions', cell: i => <span className="font-mono">{i.getValue() as number}</span> },
  { accessorKey: 'memberSince', header: 'Member since' },
  {
    accessorKey: 'active', header: 'Status',
    cell: i => i.getValue() ? <Badge variant="success">Active</Badge> : <Badge variant="secondary">Inactive</Badge>,
  },
  {
    id: '_link', header: '',
    cell: i => (
      <Link to="/users/$userId" params={{ userId: String(i.row.original.id) }}
        className="flex justify-end text-muted-foreground hover:text-foreground">
        <ChevronRight className="h-4 w-4" />
      </Link>
    ),
  },
]

export function UsersPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['users'], queryFn: api.users })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Users</h1>
        {data && <span className="text-sm text-muted-foreground">{data.pagination.total} total</span>}
      </div>
      <DataTable columns={columns} data={data?.data ?? []} isLoading={isLoading} error={error} />
    </div>
  )
}
