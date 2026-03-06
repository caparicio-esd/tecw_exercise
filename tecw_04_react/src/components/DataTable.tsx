import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from '@tanstack/react-table'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table'

interface DataTableProps<TData> {
  columns: ColumnDef<TData, unknown>[]
  data: TData[]
  isLoading?: boolean
  error?: Error | null
}

export function DataTable<TData>({ columns, data, isLoading, error }: DataTableProps<TData>) {
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })

  if (isLoading) {
    return (
      <div className="flex h-48 items-center justify-center text-muted-foreground text-sm">
        Loading…
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex h-48 items-center justify-center text-destructive text-sm">
        Error: {error.message}
      </div>
    )
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map(hg => (
            <TableRow key={hg.id}>
              {hg.headers.map(header => (
                <TableHead key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.length ? (
            table.getRowModel().rows.map(row => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map(cell => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center text-muted-foreground">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}
