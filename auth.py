from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os

API_KEY = os.getenv("API_KEY", "secret-api-key-2024")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifica la validità della API key per le operazioni protette"""
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key non valida o mancante"
        )
    return api_key