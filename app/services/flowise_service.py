import httpx

from app.utils.logger import logger
from app.utils.config import FLOWISE_API_URL
from app.utils.config import FLOWISE_HEALTH_URL
from typing import cast

class FlowiseService:

    def __init__(self)->None:
        pass

    async def predict(self, query: str):
        payload = {
            "question" : query
        }
        logger.info("Sending request to Flowise Cloud")
        try:
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
        except Exception:
            logger.exception("Flowise prediction failed")
            raise
    async def check_connection(self)->bool:
        try:
            # ping_url = cast(str,FLOWISE_API_URL).split("/prediction")[0]+"/ping"
            ping_url = cast(str,FLOWISE_HEALTH_URL)
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(ping_url)
            return response.status_code == 200
        except httpx.HTTPError:
            logger.exception("Flowise health check failed")
            return False