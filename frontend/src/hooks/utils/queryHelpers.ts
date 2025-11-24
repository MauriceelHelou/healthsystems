/**
 * React Query helper utilities.
 * Provides consistent patterns for mutations and queries.
 */
import { useMutation, useQuery, UseMutationOptions, UseQueryOptions } from '@tanstack/react-query';
import { apiClient, ApiError } from '../../utils/api';

/**
 * Default error handler for mutations.
 */
function defaultErrorHandler(error: unknown, context?: string) {
  console.error(`${context || 'Operation'} failed:`, error);

  if (error instanceof ApiError) {
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
  options?: Omit<UseMutationOptions<TData, Error, TVariables, unknown>, 'mutationFn'>
) {
  const { onError: userOnError, ...restOptions } = options || {};

  return useMutation<TData, Error, TVariables, unknown>({
    mutationFn: async (variables: TVariables) => {
      return apiClient.post<TData, TVariables>(endpoint, variables);
    },
    onError: ((error: Error, variables: TVariables, context: unknown) => {
      defaultErrorHandler(error, (options?.meta as any)?.errorContext);
      if (userOnError) {
        (userOnError as any)(error, variables, context);
      }
    }) as any,
    ...restOptions,
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
