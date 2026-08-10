from dotenv import load_dotenv
import os

load_dotenv()

FLOWISE_API_URL = os.getenv("FLOWISE_API_URL")
FLOWISE_HEALTH_URL = os.getenv("FLOWISE_HEALTH_URL")

APP_NAME = "BQBYTE AI Gateway"
VERSION = "1.0.0"