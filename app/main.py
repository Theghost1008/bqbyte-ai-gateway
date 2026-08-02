from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.utils.config import APP_NAME, VERSION

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Production-ready AI Gateway built on Flowise"
)

app.include_router(health_router)
app.include_router(predict_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BQBYTE AI Gateway 🚀"
    }