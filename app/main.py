from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.utils.config import APP_NAME, VERSION
from app.exceptions.handlers import register_exception_handler
from app.utils.exception_handler import global_exception_handler
from app.middlewares.logging import RequestLoggingMiddleware

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Production-ready AI Gateway built on Flowise"
)
app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(Exception,global_exception_handler)
register_exception_handler(app)

app.include_router(health_router)
app.include_router(predict_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BQBYTE AI Gateway 🚀"
    }