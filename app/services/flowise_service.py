from typing import Any
from app.utils.logger import logger

class FlowiseService:

    def __init__(self)->None:
        pass

    async def predict(self, query: str)->dict[str,Any]:

        # to be implemented
        logger.info(f"Received query: {query}")
        response = {
            "success": True,
            "res": f"Received query: {query}"
        }
        logger.info("Prediction generated successfully")
        return response