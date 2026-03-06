import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { api } from '@/lib/api'
import { BackLink, InfoCard, Field, SectionTitle, AssetPreview } from '@/components/Detail'

export function PlaceDetailPage() {
  const { placeId } = useParams({ from: '/places/$placeId' })
  const { data, isLoading, error } = useQuery({
    queryKey: ['places', placeId],
    queryFn: () => api.placeById(Number(placeId)),
  })

  if (isLoading) return <div className="flex h-48 items-center justify-center text-muted-foreground text-sm">Loading…</div>
  if (error || !data) return <div className="flex h-48 items-center justify-center text-destructive text-sm">{String(error)}</div>

  return (
    <div className="space-y-6">
      <BackLink to="/places" label="Places" />

      <h1 className="text-3xl font-bold">{data.name}</h1>

      <InfoCard>
        <Field label="Name">{data.name}</Field>
        <Field label="Description">
          <span className="text-muted-foreground">{data.description ?? '—'}</span>
        </Field>
      </InfoCard>

      {data.mainAsset && (
        <div className="space-y-2">
          <SectionTitle>Media</SectionTitle>
          <AssetPreview url={data.mainAsset.url} />
        </div>
      )}
    </div>
  )
}
