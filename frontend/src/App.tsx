import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Import components (to be created)
// import Header from './components/Header';
// import Footer from './components/Footer';
// import Home from './pages/Home';
// import MechanismExplorer from './pages/MechanismExplorer';
// import ContextBuilder from './pages/ContextBuilder';
// import Visualization from './pages/Visualization';

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
        <div className="min-h-screen flex flex-col">
          {/* <Header /> */}

          <main id="main-content" className="flex-grow">
            <Routes>
              <Route path="/" element={<HomePage />} />
              {/*
              <Route path="/mechanisms" element={<MechanismExplorer />} />
              <Route path="/context" element={<ContextBuilder />} />
              <Route path="/visualize" element={<Visualization />} />
              */}
            </Routes>
          </main>

          {/* <Footer /> */}
        </div>
      </Router>
    </QueryClientProvider>
  );
}

// Temporary home page component
function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-primary-700 mb-4">
        HealthSystems Platform
      </h1>
      <p className="text-lg text-gray-700 mb-6">
        Decision support platform for quantifying how structural interventions
        propagate through social-spatial-biological systems to affect health outcomes.
      </p>
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-3">Platform Features</h2>
        <ul className="space-y-2">
          <li className="flex items-start">
            <span className="text-primary-600 mr-2">✓</span>
            <span>Self-configuring geographic analysis</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary-600 mr-2">✓</span>
            <span>Bayesian mechanism weighting</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary-600 mr-2">✓</span>
            <span>Interactive systems visualizations</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary-600 mr-2">✓</span>
            <span>Transparent uncertainty quantification</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default App;
