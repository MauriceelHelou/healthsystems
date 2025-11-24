import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

/**
 * Create a new QueryClient for each test to ensure isolation
 */
export const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Don't retry failed queries in tests
        gcTime: 0, // Don't cache in tests (renamed from cacheTime in v5)
        staleTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  });

/**
 * All providers wrapper for testing
 */
interface AllProvidersProps {
  children: React.ReactNode;
  queryClient?: QueryClient;
}

export const AllProviders: React.FC<AllProvidersProps> = ({
  children,
  queryClient = createTestQueryClient(),
}) => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
};

/**
 * Custom render function that includes all providers
 */
interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  queryClient?: QueryClient;
  route?: string;
}

export const renderWithProviders = (
  ui: ReactElement,
  {
    queryClient = createTestQueryClient(),
    route = '/',
    ...renderOptions
  }: CustomRenderOptions = {}
) => {
  // Set initial route
  window.history.pushState({}, 'Test page', route);

  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <AllProviders queryClient={queryClient}>{children}</AllProviders>
  );

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    queryClient,
  };
};

/**
 * Wait for loading states to complete
 */
export const waitForLoadingToFinish = () => {
  return new Promise((resolve) => setTimeout(resolve, 0));
};

// Re-export everything from React Testing Library
export * from '@testing-library/react';
export { renderWithProviders as render };
