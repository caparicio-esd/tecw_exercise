import { createRouter, createRoute, createRootRoute, Navigate, Outlet } from '@tanstack/react-router'
import { Layout } from './components/Layout'
import { WaysPage }            from './pages/WaysPage'
import { WayDetailPage }       from './pages/WayDetailPage'
import { BlocksPage }          from './pages/BlocksPage'
import { BlockDetailPage }     from './pages/BlockDetailPage'
import { PlacesPage }          from './pages/PlacesPage'
import { PlaceDetailPage }     from './pages/PlaceDetailPage'
import { UsersPage }           from './pages/UsersPage'
import { UserDetailPage }      from './pages/UserDetailPage'
import { ActivityRecordsPage } from './pages/ActivityRecordsPage'
import { ActivityRecordDetailPage } from './pages/ActivityRecordDetailPage'

const rootRoute = createRootRoute({
  component: () => (
    <Layout>
      <Outlet />
    </Layout>
  ),
})

const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: '/',
  component: () => <Navigate to="/ways" /> })

// Ways
const waysRoute      = createRoute({ getParentRoute: () => rootRoute, path: '/ways',          component: WaysPage })
const wayDetailRoute = createRoute({ getParentRoute: () => rootRoute, path: '/ways/$wayId',   component: WayDetailPage })

// Blocks
const blocksRoute      = createRoute({ getParentRoute: () => rootRoute, path: '/blocks',           component: BlocksPage })
const blockDetailRoute = createRoute({ getParentRoute: () => rootRoute, path: '/blocks/$blockId',  component: BlockDetailPage })

// Places
const placesRoute      = createRoute({ getParentRoute: () => rootRoute, path: '/places',           component: PlacesPage })
const placeDetailRoute = createRoute({ getParentRoute: () => rootRoute, path: '/places/$placeId',  component: PlaceDetailPage })

// Users
const usersRoute      = createRoute({ getParentRoute: () => rootRoute, path: '/users',          component: UsersPage })
const userDetailRoute = createRoute({ getParentRoute: () => rootRoute, path: '/users/$userId',  component: UserDetailPage })

// Activity records
const activityRoute      = createRoute({ getParentRoute: () => rootRoute, path: '/activity-records',              component: ActivityRecordsPage })
const activityDetailRoute= createRoute({ getParentRoute: () => rootRoute, path: '/activity-records/$recordId',    component: ActivityRecordDetailPage })

const routeTree = rootRoute.addChildren([
  indexRoute,
  waysRoute, wayDetailRoute,
  blocksRoute, blockDetailRoute,
  placesRoute, placeDetailRoute,
  usersRoute, userDetailRoute,
  activityRoute, activityDetailRoute,
])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}
