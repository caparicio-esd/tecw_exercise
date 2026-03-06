import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from '@tanstack/react-router'
import { api } from '@/lib/api'
import { Badge } from '@/components/ui/badge'
import { BackLink, InfoCard, Field, SectionTitle, AssetPreview } from '@/components/Detail'

export function ActivityRecordDetailPage() {
  const { recordId } = useParams({ from: '/activity-records/$recordId' })
  const { data, isLoading, error } = useQuery({
    queryKey: ['activity-records', recordId],
    queryFn: () => api.activityRecordById(Number(recordId)),
  })

  if (isLoading) return <div className="flex h-48 items-center justify-center text-muted-foreground text-sm">Loading…</div>
  if (error || !data) return <div className="flex h-48 items-center justify-center text-destructive text-sm">{String(error)}</div>

  return (
    <div className="space-y-6">
      <BackLink to="/activity-records" label="Activity Records" />

      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-3xl font-bold">Record #{data.id}</h1>
        <span className="font-mono text-muted-foreground">{data.date}</span>
      </div>

      <InfoCard>
        <Field label="Date"><span className="font-mono">{data.date}</span></Field>
        <Field label="Notes"><span className="text-muted-foreground">{data.notes ?? '—'}</span></Field>
      </InfoCard>

      {/* Relations */}
      <div className="grid gap-4 md:grid-cols-2">

        {data.user && (
          <div className="rounded-lg border p-4 space-y-2">
            <SectionTitle>User</SectionTitle>
            <Link
              to="/users/$userId"
              params={{ userId: String(data.user.id) }}
              className="flex items-center gap-2 hover:underline"
            >
              <span className="text-2xl">{data.user.avatar}</span>
              <span className="font-medium">{data.user.name}</span>
            </Link>
          </div>
        )}

        {data.way && (
          <div className="rounded-lg border p-4 space-y-2">
            <SectionTitle>Way</SectionTitle>
            <Link
              to="/ways/$wayId"
              params={{ wayId: String(data.way.id) }}
              className="flex items-center gap-2 hover:underline"
            >
              <Badge variant="outline">{data.way.grade}</Badge>
              <span className="font-medium">{data.way.name}</span>
              <Badge variant="secondary">{data.way.type}</Badge>
            </Link>
            <p className="text-sm text-muted-foreground capitalize">{data.way.city}</p>
          </div>
        )}

        {data.block && (
          <div className="rounded-lg border p-4 space-y-2">
            <SectionTitle>Block</SectionTitle>
            <Link
              to="/blocks/$blockId"
              params={{ blockId: String(data.block.id) }}
              className="flex items-center gap-2 hover:underline"
            >
              <Badge variant="outline">{data.block.grade}</Badge>
              <span className="font-medium">{data.block.name}</span>
              <span className="h-3 w-3 rounded-full border" style={{ backgroundColor: data.block.color }} />
            </Link>
            <p className="text-sm text-muted-foreground capitalize">{data.block.city}</p>
          </div>
        )}
      </div>

      {data.mainAsset && (
        <div className="space-y-2">
          <SectionTitle>Media</SectionTitle>
          <AssetPreview url={data.mainAsset.url} />
        </div>
      )}
    </div>
  )
}
