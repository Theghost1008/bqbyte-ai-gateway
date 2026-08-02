from pydantic import BaseModel

class PredictionRes(BaseModel):
    success:bool
    res: str