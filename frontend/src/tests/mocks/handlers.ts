import { http, HttpResponse } from 'msw';
import { mockApiResponses, mockMechanisms, getMockMechanism } from './mockData';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

/**
 * Mock Service Worker handlers for API endpoints
 */
export const handlers = [
  // GET /api/mechanisms - List mechanisms
  http.get(`${API_BASE_URL}/api/mechanisms`, ({ request }) => {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    const skip = parseInt(url.searchParams.get('skip') || '0');
    const limit = parseInt(url.searchParams.get('limit') || '20');

    let filteredMechanisms = mockMechanisms;

    // Filter by category if provided
    if (category) {
      filteredMechanisms = filteredMechanisms.filter((m) => m.category === category);
    }

    // Apply pagination
    const paginatedMechanisms = filteredMechanisms.slice(skip, skip + limit);

    return HttpResponse.json({
      items: paginatedMechanisms,
      total: filteredMechanisms.length,
      skip,
      limit,
    });
  }),

  // GET /api/mechanisms/:id - Get single mechanism
  http.get(`${API_BASE_URL}/api/mechanisms/:id`, ({ params }) => {
    const { id } = params;
    const mechanism = getMockMechanism(id as string);

    if (!mechanism) {
      return HttpResponse.json(
        { detail: `Mechanism ${id} not found` },
        { status: 404 }
      );
    }

    return HttpResponse.json(mechanism);
  }),

  // GET /api/mechanisms/stats/summary - Get statistics
  http.get(`${API_BASE_URL}/api/mechanisms/stats/summary`, () => {
    return HttpResponse.json(mockApiResponses.stats);
  }),

  // GET /api/mechanisms/search/pathway - Search pathways
  http.get(`${API_BASE_URL}/api/mechanisms/search/pathway`, ({ request }) => {
    const url = new URL(request.url);
    const source = url.searchParams.get('source_node');
    const target = url.searchParams.get('target_node');

    let results = mockMechanisms;

    if (source) {
      results = results.filter((m) => m.source_node === source);
    }

    if (target) {
      results = results.filter((m) => m.target_node === target);
    }

    return HttpResponse.json({
      pathways: results,
      count: results.length,
    });
  }),

  // POST /api/mechanisms - Create mechanism (admin)
  http.post(`${API_BASE_URL}/api/mechanisms`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      {
        ...body,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      { status: 201 }
    );
  }),

  // PUT /api/mechanisms/:id - Update mechanism (admin)
  http.put(`${API_BASE_URL}/api/mechanisms/:id`, async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();
    const mechanism = getMockMechanism(id as string);

    if (!mechanism) {
      return HttpResponse.json(
        { detail: `Mechanism ${id} not found` },
        { status: 404 }
      );
    }

    return HttpResponse.json({
      ...mechanism,
      ...body,
      updated_at: new Date().toISOString(),
    });
  }),

  // DELETE /api/mechanisms/:id - Delete mechanism (admin)
  http.delete(`${API_BASE_URL}/api/mechanisms/:id`, ({ params }) => {
    const { id } = params;
    const mechanism = getMockMechanism(id as string);

    if (!mechanism) {
      return HttpResponse.json(
        { detail: `Mechanism ${id} not found` },
        { status: 404 }
      );
    }

    return new HttpResponse(null, { status: 204 });
  }),
];

/**
 * Error handlers for testing error states
 */
export const errorHandlers = [
  http.get(`${API_BASE_URL}/api/mechanisms`, () => {
    return HttpResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }),

  http.get(`${API_BASE_URL}/api/mechanisms/:id`, () => {
    return HttpResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }),
];

/**
 * Network error handlers for testing network failures
 */
export const networkErrorHandlers = [
  http.get(`${API_BASE_URL}/api/mechanisms`, () => {
    return HttpResponse.error();
  }),

  http.get(`${API_BASE_URL}/api/mechanisms/:id`, () => {
    return HttpResponse.error();
  }),
];
