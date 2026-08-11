from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.logger import logger

async def global_exception_handler(request:Request,exc:Exception):
    logger.exception("Unhandled exception | method=%s | path=%s",request.method,request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "success":False,
            "error":"Internal Server Error"
        }
    )