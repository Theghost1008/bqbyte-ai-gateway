import time

from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        start=time.perf_counter()
        logger.info(f"Incoming request | {request.method} {request.url.path}")
        response = await call_next(request)
        duration = (time.perf_counter()-start)*1000
        logger.info(f"Completed | {request.method} {request.url.path} |" f"Status={response.status_code} |" f"{duration:.2f} ms")
        return response