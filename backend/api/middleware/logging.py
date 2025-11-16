"""
Logging middleware for request/response tracking.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process each request and log details.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response
        """
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"for {request.method} {request.url.path} "
            f"in {process_time:.3f}s"
        )

        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)

        return response
