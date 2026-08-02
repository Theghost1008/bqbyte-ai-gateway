from fastapi import APIRouter

from app.models.request import PredictionReq
from app.models.response import PredictionRes
from app.services.flowise_service import FlowiseService
from app.utils.logger import logger

router = APIRouter()

service = FlowiseService()

@router.post("/predict", response_model=PredictionRes)
async def predict(req: PredictionReq):
    logger.info("Prediction endpoint called")
    result = await service.predict(req.query)
    logger.info("Prediction endpoint completed")
    return result