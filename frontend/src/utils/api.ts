/**
 * Unified API client for backend communication.
 * Centralizes fetch logic, error handling, and endpoint management.
 */

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

export const API_ENDPOINTS = {
  // Node endpoints
  nodes: {
    // Note: Direct node list/detail endpoints exist in backend but are not currently used.
    // Nodes are currently accessed implicitly through mechanisms.
    // Uncomment below if node management UI is needed in the future:
    // list: '/api/nodes',
    // detail: (id: string) => `/api/nodes/${id}`,
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
    // Note: Backend also has '/api/pathways/search' endpoint for keyword search
    // Add here if search UI is implemented: search: '/api/pathways/search',
  },
} as const;

// Response types
export interface ApiResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
}

export interface ApiErrorResponse {
  detail?: string;
  message?: string;
  status: number;
  statusText: string;
}

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
