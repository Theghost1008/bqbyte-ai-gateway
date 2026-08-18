from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.flowise_exception import (FlowiseConnectionError,FlowiseResponseError,FlowiseTimeoutError)

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

async def flowise_timeout_handler(request:Request, exc:FlowiseTimeoutError):
    logger.error("Flowise timeout | path=%s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "success":False,
            "error":"Flowise Service timed out"
        }        
    )

async def flowise_connecion_handler(request:Request, exc: FlowiseConnectionError):
    logger.error("Flowise connection failure | path=%s", request.url.path)
    return JSONResponse(
        status_code=503,
        content={
            "success":False,
            "error":"Flowise Service is unavailable"
        }
    )

async def flowise_response_handler(request:Request, exc: FlowiseResponseError):
    logger.error("Flowise returned an error response | path=%s", request.url.path)
    return JSONResponse(
        status_code=502,
        content={
            "success":False,
            "error":"Flowise service returned an error"
        }
    )