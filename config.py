#openssl rand -hex 32

from fastapi.security import OAuth2PasswordBearer




SECRET_KEY = "88587323f737e015344250f2f8958811c6a9c3a049f9bf77bb324975c265c64a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
