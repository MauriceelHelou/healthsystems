"""
Rate limiting middleware to prevent API abuse.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
from collections import defaultdict
import asyncio

from api.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting.
    For production, use Redis-based rate limiting.
    """

    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
        self.lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Check rate limit before processing request.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        async with self.lock:
            # Clean old requests (older than 1 minute)
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < 60
            ]

            # Check rate limit
            if len(self.requests[client_ip]) >= settings.rate_limit_per_minute:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )

            # Add current request
            self.requests[client_ip].append(current_time)

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.rate_limit_per_minute - len(self.requests[client_ip])
        )

        return response
