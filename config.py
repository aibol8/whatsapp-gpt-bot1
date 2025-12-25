import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOOKING_LINK = os.getenv("BOOKING_LINK")
SALON_NAME = os.getenv("SALON_NAME")
