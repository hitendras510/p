import os


class Settings:
    APP_NAME = "EcoRoute AI"
    VERSION = "1.0"

    # Model settings
    MODEL_PATH = os.getenv("MODEL_PATH", "models/eco_model.pkl")

    # API settings
    DEBUG = True


settings = Settings()