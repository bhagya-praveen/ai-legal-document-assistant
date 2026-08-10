import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///legal_ai.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

   