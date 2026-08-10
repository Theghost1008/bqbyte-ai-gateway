from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.services.flowise_service import FlowiseService

service = FlowiseService()

router = APIRouter(
    prefix="",
    tags=["Health"]
)


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "BQBYTE AI Gateway",
        "version": "1.0.0"
    }
@router.get("/ready")
async def readiness_check():
    is_ready = await service.check_connection()

    if not is_ready:
        return JSONResponse(
            status_code=503,
            content={
                "status":"not_ready",
                "service":"BQBYTE AI Gateway"
            }
        )
    return {
        "status":"ready",
        "service":"BQBYTE AI Gateway"
    }