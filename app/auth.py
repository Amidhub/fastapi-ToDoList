import os
from authx import AuthX, AuthXConfig
from pydantic import Extra

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret_change_me")

class MyAuthConfig(AuthXConfig):
    model_config = {"extra": Extra.allow}

config = MyAuthConfig()
config.secret_key = SECRET_KEY
config.algorithm = "HS256"
config.access_token_expires_minutes = 60

# Инициализируем AuthX
auth = AuthX(config=config)