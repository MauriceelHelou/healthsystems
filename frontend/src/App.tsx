import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardLayout } from './layouts/DashboardLayout';
import { SystemsMapView } from './views/SystemsMapView';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <DashboardLayout>
          <Routes>
            <Route path="/" element={<SystemsMapView />} />
            <Route path="/pathways" element={<PathwayExplorerPlaceholder />} />
            <Route path="/library" element={<LibraryPlaceholder />} />
          </Routes>
        </DashboardLayout>
      </Router>
    </QueryClientProvider>
  );
}

// Placeholder components for other views
function PathwayExplorerPlaceholder() {
  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Pathway Explorer</h2>
        <p className="text-gray-600">Coming soon...</p>
      </div>
    </div>
  );
}

function LibraryPlaceholder() {
  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Node Library</h2>
        <p className="text-gray-600">Coming soon...</p>
      </div>
    </div>
  );
}

export default App;
