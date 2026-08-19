import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.utils.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        start=time.perf_counter()
        logger.info(f"[%s] Incoming request | %s %s", request_id,request.method,request.url.path)
        response = await call_next(request)
        duration = (time.perf_counter()-start)*1000
        logger.info(f"[%s]Completed | %s | %.2f ms",request_id,response.status_code,duration)
        response.headers["X-request-ID"] = request_id
        return response