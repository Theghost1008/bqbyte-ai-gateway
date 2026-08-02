from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter(
    prefix="",
    tags=["Health"]
)


@router.get("/health")
async def health_check():
    logger.info("Health endpoint called")
    return {
        "status": "healthy",
        "service": "BQBYTE AI Gateway",
        "version": "1.0.0"
    }