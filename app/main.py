from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.utils.config import settings
from app.exceptions.handlers import register_exception_handler
# from app.utils.exception_handler import (global_exception_handler,flowise_timeout_handler,flowise_connecion_handler,flowise_response_handler)
from app.middlewares.logging import RequestLoggingMiddleware
# from app.exceptions.flowise_exception import (FlowiseConnectionError,FlowiseResponseError,FlowiseTimeoutError)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Production-ready AI Gateway built on Flowise"
)
app.add_middleware(RequestLoggingMiddleware)
register_exception_handler(app)

app.include_router(health_router)
app.include_router(predict_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BQBYTE AI Gateway 🚀"
    }