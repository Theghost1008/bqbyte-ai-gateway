import httpx
from typing import Any
from app.utils.logger import logger
from app.utils.config import FLOWISE_API_URL
from typing import cast

class FlowiseService:

    def __init__(self)->None:
        pass

    async def predict(self, query: str):
        payload = {
            "question" : query
        }
        logger.info("Sending request to Flowise Cloud")
        async with httpx.AsyncClient(timeout=30.0) as client :
            response = await client.post(cast(str,FLOWISE_API_URL),json=payload)
        response.raise_for_status()
        data=response.json()
        logger.info(f"Flowise response received | chatId={data.get('chatId')} | sessionId={data.get('sessionId')}")
        logger.info("Received response from Flowise")
        return {
            "success": True,
            "res": data.get("text","No response returned")
        }
            