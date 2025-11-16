/**
 * API client for HealthSystems backend.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Create axios instance with default configuration.
 */
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor for adding auth tokens, etc.
 */
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Response interceptor for error handling.
 */
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle specific error codes
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    } else if (error.response?.status === 429) {
      // Rate limit exceeded
      console.error('Rate limit exceeded. Please try again later.');
    }
    return Promise.reject(error);
  }
);

export default api;

/**
 * API service methods
 */

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Mechanism endpoints (to be implemented)
export const mechanismsApi = {
  getAll: async () => {
    const response = await api.get('/api/mechanisms');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/api/mechanisms/${id}`);
    return response.data;
  },
  search: async (query: string) => {
    const response = await api.get('/api/mechanisms/search', {
      params: { q: query },
    });
    return response.data;
  },
};

// Context endpoints (to be implemented)
export const contextsApi = {
  create: async (data: any) => {
    const response = await api.post('/api/contexts', data);
    return response.data;
  },
  getByGeography: async (geography: string) => {
    const response = await api.get(`/api/contexts/${geography}`);
    return response.data;
  },
};

// Weights endpoints (to be implemented)
export const weightsApi = {
  calculate: async (mechanismId: string, contextData: any) => {
    const response = await api.post('/api/weights/calculate', {
      mechanism_id: mechanismId,
      context_data: contextData,
    });
    return response.data;
  },
};
