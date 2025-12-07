import { FC, lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardLayout } from './layouts/DashboardLayout';
import { SystemsMapView } from './views/SystemsMapView';
import { MetadataDrivenSystemView } from './views/MetadataDrivenSystemView';
import { ImportantNodesView } from './views/ImportantNodesView';
// Temporarily disabled
// import { PathfinderView } from './views/PathfinderView';
// import { PathwayExplorerView } from './views/PathwayExplorerView';
import { CrisisExplorerView } from './views/CrisisExplorerView';
import type { Category, NodeScale } from './types/mechanism';

// Lazy load marketing page to avoid bundling with main app
const HomePage = lazy(() => import('./pages/marketing/HomePage'));

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

// Loading fallback for lazy-loaded components
const LoadingFallback = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4" />
      <p className="text-gray-600">Loading...</p>
    </div>
  </div>
);

const App: FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Marketing home page - no DashboardLayout */}
          <Route
            path="/"
            element={
              <Suspense fallback={<LoadingFallback />}>
                <HomePage />
              </Suspense>
            }
          />

          {/* Systems Map (moved from /) */}
          <Route
            path="/systems"
            element={
              <DashboardLayout>
                <SystemsMapView />
              </DashboardLayout>
            }
          />
          <Route
            path="/systems/alcoholism"
            element={
              <DashboardLayout>
                <MetadataDrivenSystemView
                  title="Alcoholism System Analysis"
                  description="Explore causal pathways related to alcohol use disorder and liver disease (showing nodes with 2+ connections)"
                  domainKeywords={[
                    'alcohol', 'ald', 'liver', 'drinking', 'substance', 'addiction',
                    'hepatitis', 'cirrhosis', 'binge', 'aud', 'liquor', 'beer', 'wine',
                    'intoxication', 'alcoholic', 'abuse', 'dependence', 'withdrawal',
                    'detox', 'recovery', 'sobriety', 'tavern', 'bar', 'pub',
                  ]}
                  initialCategories={[
                    'economic', 'behavioral', 'healthcare_access', 'biological',
                    'social_environment', 'political', 'built_environment',
                  ] as Category[]}
                  initialScales={[1, 2, 3, 4, 5, 6, 7] as NodeScale[]}
                  minConnections={2}
                />
              </DashboardLayout>
            }
          />
          <Route
            path="/important-nodes"
            element={
              <DashboardLayout>
                <ImportantNodesView />
              </DashboardLayout>
            }
          />
          {/* Temporarily disabled
          <Route path="/pathfinder" element={<DashboardLayout><PathfinderView /></DashboardLayout>} />
          <Route path="/pathways" element={<DashboardLayout><PathwayExplorerView /></DashboardLayout>} />
          */}
          <Route
            path="/crisis-explorer"
            element={
              <DashboardLayout>
                <CrisisExplorerView />
              </DashboardLayout>
            }
          />
          {/* <Route path="/library" element={<DashboardLayout><LibraryPlaceholder /></DashboardLayout>} /> */}
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

// Placeholder components for other views - temporarily disabled
// function LibraryPlaceholder() {
//   return (
//     <div className="flex-1 flex items-center justify-center bg-gray-50">
//       <div className="text-center">
//         <h2 className="text-2xl font-bold text-gray-900 mb-2">Node Library</h2>
//         <p className="text-gray-600">Coming soon...</p>
//       </div>
//     </div>
//   );
// }

export default App;
