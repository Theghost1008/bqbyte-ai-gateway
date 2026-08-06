from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
import httpx

from app.utils.logger import logger

def register_exception_handler(app: FastAPI):
    @app.exception_handler(httpx.TimeoutException)
    async def timeout_exception_handler(request: Request, exc: httpx.TimeoutException):
        logger.error(f"Flowise timeout:{exc}")

        return JSONResponse(
            status_code=504,
            content={
                "success":False,
                "message":"Flowise service timed out"
            }
        )
    @app.exception_handler(httpx.HTTPStatusError)
    async def http_status_handler(request: Request, exc: httpx.TimeoutException):
        logger.error(f"Flowise HTTP error:{exc}")

        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "message": "Flowise returned an invalid response"
            }
        )
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request:Request, exc:HTTPException):
        logger.error(f"HTTP Exception: {exc.detail}")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success":False,
                "message":exc.detail
            }
        )
    @app.exception_handler(Exception)
    async def global_exception_handler(request:Request, exc:HTTPException):
        logger.error("Unhandled exception")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message":"Internal server error"
            }
        )