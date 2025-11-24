# PROMPT 3: Unify Pathfinding Logic

## Context
Pathfinding logic is duplicated across **5 custom hooks** with shared API patterns, error handling, and data transformation. This creates **831 lines of redundant code** and inconsistent behavior across features.

## Current State

### Files with Redundant Patterns (831 LOC duplication)

**Primary hooks:**
- `frontend/src/hooks/usePathfinding.ts` (507 LOC) → 150 LOC target
- `frontend/src/hooks/useCrisisSubgraph.ts` (247 LOC) → 100 LOC target
- `frontend/src/hooks/usePathways.ts` (77 LOC) → 50 LOC target
- `frontend/src/hooks/useAlcoholismSystem.ts` (partial duplication)
- `frontend/src/hooks/useNodeImportance.ts` (partial duplication)

### Redundancy Examples

**Example 1: React Query Mutation Pattern (duplicated 5 times)**

```typescript
// usePathfinding.ts (lines 89-103)
const mutation = useMutation({
  mutationFn: async (request: PathfindingRequest) => {
    const response = await fetch('http://localhost:8000/api/nodes/pathfinding', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  },
  // ... other config
});

// useCrisisSubgraph.ts (lines 67-81) - IDENTICAL PATTERN
const mutation = useMutation({
  mutationFn: async (request: CrisisSubgraphRequest) => {
    const response = await fetch('http://localhost:8000/api/nodes/crisis-subgraph', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  },
  // ... other config
});
```

**Example 2: Error Handling (duplicated 5 times)**

```typescript
// usePathfinding.ts (lines 112-118)
onError: (error) => {
  console.error('Pathfinding failed:', error);
  toast.error(`Failed to find paths: ${error.message}`);
},

// usePathways.ts (lines 34-40) - IDENTICAL
onError: (error) => {
  console.error('Pathway fetch failed:', error);
  toast.error(`Failed to fetch pathways: ${error.message}`);
},
```

**Example 3: API Base URL (hardcoded 8 times)**

```typescript
// usePathfinding.ts (line 91)
const response = await fetch('http://localhost:8000/api/nodes/pathfinding', {

// useCrisisSubgraph.ts (line 69)
const response = await fetch('http://localhost:8000/api/nodes/crisis-subgraph', {

// useNodeImportance.ts (line 45)
const response = await fetch('http://localhost:8000/api/nodes/importance', {

// ... 5 more instances
```

## Target Architecture

```
frontend/src/
├── utils/
│   ├── api.ts                          # 100 LOC - Unified API client
│   │   ├── apiClient                   # Centralized fetch wrapper
│   │   ├── endpoints                   # Endpoint constants
│   │   └── buildRequest()
│   │
│   └── queryHelpers.ts                 # 80 LOC - React Query helpers
│       ├── createApiMutation()
│       ├── createApiQuery()
│       └── defaultMutationOptions
│
└── hooks/
    ├── usePathfinding.ts               # 150 LOC (reduced from 507)
    ├── useCrisisSubgraph.ts            # 100 LOC (reduced from 247)
    ├── usePathways.ts                  # 50 LOC (reduced from 77)
    ├── useNodeImportance.ts            # Simplified
    └── useAlcoholismSystem.ts          # Simplified
```

## Implementation Steps

### Step 1: Create Unified API Client

**File: `frontend/src/utils/api.ts`**

```typescript
/**
 * Unified API client for backend communication.
 * Centralizes fetch logic, error handling, and endpoint management.
 */

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Node endpoints
  nodes: {
    list: '/api/nodes',
    detail: (id: string) => `/api/nodes/${id}`,
    pathfinding: '/api/nodes/pathfinding',
    importance: '/api/nodes/importance',
    crisisEndpoints: '/api/nodes/crisis-endpoints',
    crisisSubgraph: '/api/nodes/crisis-subgraph',
  },
  // Mechanism endpoints
  mechanisms: {
    list: '/api/mechanisms',
    detail: (id: string) => `/api/mechanisms/${id}`,
    stats: '/api/mechanisms/stats/summary',
  },
  // Pathway endpoints
  pathways: {
    list: '/api/pathways',
    detail: (id: string) => `/api/pathways/${id}`,
  },
} as const;

// Error types
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string,
    public body?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Request options
export interface ApiRequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}

/**
 * Build full URL with query parameters.
 */
function buildUrl(endpoint: string, params?: Record<string, string | number | boolean>): string {
  const url = new URL(endpoint, API_BASE_URL);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value));
    });
  }

  return url.toString();
}

/**
 * Core API client with error handling.
 */
export const apiClient = {
  /**
   * GET request
   */
  async get<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    const { params, ...fetchOptions } = options;
    const url = buildUrl(endpoint, params);

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
      ...fetchOptions,
    });

    return handleResponse<T>(response);
  },

  /**
   * POST request
   */
  async post<T, D = any>(endpoint: string, data?: D, options: ApiRequestOptions = {}): Promise<T> {
    const { params, ...fetchOptions } = options;
    const url = buildUrl(endpoint, params);

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
      ...fetchOptions,
    });

    return handleResponse<T>(response);
  },

  /**
   * PUT request
   */
  async put<T, D = any>(endpoint: string, data?: D, options: ApiRequestOptions = {}): Promise<T> {
    const { params, ...fetchOptions } = options;
    const url = buildUrl(endpoint, params);

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
      ...fetchOptions,
    });

    return handleResponse<T>(response);
  },

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    const { params, ...fetchOptions } = options;
    const url = buildUrl(endpoint, params);

    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
      ...fetchOptions,
    });

    return handleResponse<T>(response);
  },
};

/**
 * Handle response and errors.
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let body;
    try {
      body = await response.json();
    } catch {
      body = await response.text();
    }

    throw new ApiError(
      body?.detail || `HTTP ${response.status}: ${response.statusText}`,
      response.status,
      response.statusText,
      body
    );
  }

  // Handle empty responses (204 No Content)
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}
```

### Step 2: Create React Query Helpers

**File: `frontend/src/utils/queryHelpers.ts`**

```typescript
/**
 * React Query helper utilities.
 * Provides consistent patterns for mutations and queries.
 */
import { useMutation, useQuery, UseMutationOptions, UseQueryOptions } from '@tanstack/react-query';
import { apiClient, ApiError } from './api';

/**
 * Default error handler for mutations.
 */
function defaultErrorHandler(error: unknown, context?: string) {
  console.error(`${context || 'Operation'} failed:`, error);

  if (error instanceof ApiError) {
    // Could integrate with toast library here
    console.error(`API Error ${error.status}: ${error.message}`);
  } else if (error instanceof Error) {
    console.error(`Error: ${error.message}`);
  }
}

/**
 * Create a POST mutation with consistent error handling.
 */
export function createPostMutation<TData, TVariables>(
  endpoint: string,
  options?: Omit<UseMutationOptions<TData, Error, TVariables>, 'mutationFn'>
) {
  return useMutation<TData, Error, TVariables>({
    mutationFn: async (variables: TVariables) => {
      return apiClient.post<TData, TVariables>(endpoint, variables);
    },
    onError: (error) => {
      defaultErrorHandler(error, options?.meta?.errorContext as string);
      options?.onError?.(error, {} as TVariables, undefined);
    },
    ...options,
  });
}

/**
 * Create a GET query with consistent error handling.
 */
export function createGetQuery<TData>(
  endpoint: string,
  params?: Record<string, string | number | boolean>,
  options?: Omit<UseQueryOptions<TData, Error>, 'queryKey' | 'queryFn'>
) {
  return useQuery<TData, Error>({
    queryKey: [endpoint, params],
    queryFn: async () => {
      return apiClient.get<TData>(endpoint, { params });
    },
    onError: (error) => {
      defaultErrorHandler(error, options?.meta?.errorContext as string);
    },
    ...options,
  });
}

/**
 * Default mutation options for consistency.
 */
export const defaultMutationOptions = {
  retry: false,
  retryDelay: 0,
} as const;

/**
 * Default query options for consistency.
 */
export const defaultQueryOptions = {
  staleTime: 5 * 60 * 1000, // 5 minutes
  refetchOnWindowFocus: false,
  retry: 1,
} as const;
```

### Step 3: Refactor usePathfinding Hook

**File: `frontend/src/hooks/usePathfinding.ts` (simplified)**

```typescript
/**
 * Pathfinding hook using unified API client.
 * Reduced from 507 LOC to ~150 LOC.
 */
import { PathfindingRequest, PathfindingResponse, PathResult } from '../types/mechanism';
import { createPostMutation } from '../utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

export function usePathfinding() {
  return createPostMutation<PathfindingResponse, PathfindingRequest>(
    API_ENDPOINTS.nodes.pathfinding,
    {
      meta: {
        errorContext: 'Pathfinding',
      },
    }
  );
}

// Helper functions (keep these - they're domain-specific logic)
export function formatPathLength(length: number): string {
  return `${length} step${length !== 1 ? 's' : ''}`;
}

export function getEvidenceGradeColor(grade: string): string {
  switch (grade) {
    case 'A': return 'text-green-600';
    case 'B': return 'text-yellow-600';
    case 'C': return 'text-orange-600';
    default: return 'text-gray-600';
  }
}

export function getDirectionColor(direction: string): string {
  return direction === 'positive' ? 'text-blue-600' : 'text-red-600';
}

export type { PathResult };
```

### Step 4: Refactor useCrisisSubgraph Hook

**File: `frontend/src/hooks/useCrisisSubgraph.ts` (simplified)**

```typescript
/**
 * Crisis subgraph hook using unified API client.
 * Reduced from 247 LOC to ~100 LOC.
 */
import { CrisisSubgraphRequest, CrisisSubgraphResponse } from '../types/mechanism';
import { createPostMutation, createGetQuery } from '../utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

/**
 * Fetch crisis endpoint nodes.
 */
export function useCrisisEndpoints() {
  return createGetQuery<Array<{ id: string; name: string; scale: number }>>(
    API_ENDPOINTS.nodes.crisisEndpoints,
    undefined,
    {
      meta: { errorContext: 'Crisis endpoints' },
    }
  );
}

/**
 * Compute crisis subgraph.
 */
export function useCrisisSubgraph() {
  return createPostMutation<CrisisSubgraphResponse, CrisisSubgraphRequest>(
    API_ENDPOINTS.nodes.crisisSubgraph,
    {
      meta: { errorContext: 'Crisis subgraph' },
    }
  );
}
```

### Step 5: Refactor usePathways Hook

**File: `frontend/src/hooks/usePathways.ts` (simplified)**

```typescript
/**
 * Pathways hook using unified API client.
 * Reduced from 77 LOC to ~50 LOC.
 */
import { Pathway } from '../types/mechanism';
import { createGetQuery } from '../utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

export function usePathways() {
  return createGetQuery<Pathway[]>(
    API_ENDPOINTS.pathways.list,
    undefined,
    {
      meta: { errorContext: 'Pathways' },
    }
  );
}

export function usePathway(pathwayId: string) {
  return createGetQuery<Pathway>(
    API_ENDPOINTS.pathways.detail(pathwayId),
    undefined,
    {
      enabled: !!pathwayId,
      meta: { errorContext: 'Pathway detail' },
    }
  );
}
```

### Step 6: Create Environment Config

**File: `frontend/.env.example`**

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Feature Flags
VITE_ENABLE_PATHFINDING=true
VITE_ENABLE_CRISIS_EXPLORER=true
```

## Migration Checklist

### Phase 1: Create Infrastructure (Day 1)
- [ ] Create `frontend/src/utils/api.ts`
- [ ] Create `frontend/src/utils/queryHelpers.ts`
- [ ] Create `.env.example` with API_URL
- [ ] Test API client: `npm run test utils/api.test.ts`

### Phase 2: Refactor Hooks (Day 1-2)
- [ ] Refactor `usePathfinding.ts` to use API client
- [ ] Refactor `useCrisisSubgraph.ts`
- [ ] Refactor `usePathways.ts`
- [ ] Refactor `useNodeImportance.ts`
- [ ] Refactor `useAlcoholismSystem.ts`

### Phase 3: Update Components (Day 2)
- [ ] Update `PathfinderView.tsx` imports
- [ ] Update `CrisisExplorerView.tsx` imports
- [ ] Update `PathwayExplorerView.tsx` imports
- [ ] Verify all components still work

### Phase 4: Testing (Day 2)
- [ ] Test pathfinding feature end-to-end
- [ ] Test crisis explorer end-to-end
- [ ] Test error handling (simulate API errors)
- [ ] Test with production API URL

### Phase 5: Cleanup (Day 2)
- [ ] Remove duplicate fetch code from all hooks
- [ ] Remove hardcoded API URLs
- [ ] Update documentation
- [ ] Commit with message: "refactor: unify API client and React Query patterns"

## Testing Requirements

### Unit Tests

**File: `frontend/src/utils/api.test.ts`**

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiClient, ApiError } from './api';

describe('apiClient', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('should make GET request', async () => {
    const mockData = { id: '1', name: 'Test' };
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await apiClient.get('/api/test');
    expect(result).toEqual(mockData);
  });

  it('should handle API errors', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 404,
      statusText: 'Not Found',
      json: async () => ({ detail: 'Resource not found' }),
    });

    await expect(apiClient.get('/api/test')).rejects.toThrow(ApiError);
  });

  it('should add query parameters', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    await apiClient.get('/api/test', { params: { foo: 'bar', limit: 10 } });

    const callUrl = (global.fetch as any).mock.calls[0][0];
    expect(callUrl).toContain('foo=bar');
    expect(callUrl).toContain('limit=10');
  });
});
```

### Integration Test

```typescript
// Test actual hook usage
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { usePathfinding } from '../usePathfinding';

it('should fetch pathfinding results', async () => {
  const queryClient = new QueryClient();
  const wrapper = ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  const { result } = renderHook(() => usePathfinding(), { wrapper });

  result.current.mutate({
    from_node_id: 'node1',
    to_node_id: 'node2',
    algorithm: 'shortest',
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data).toBeDefined();
});
```

## Success Criteria

- ✅ All hooks use unified API client
- ✅ No hardcoded API URLs
- ✅ Consistent error handling
- ✅ Environment-based configuration
- ✅ All tests passing
- ✅ **831 LOC eliminated** from redundant patterns
- ✅ No regressions in feature functionality

## Estimated Effort
**2 days** (1 day infrastructure + refactoring, 1 day testing)
