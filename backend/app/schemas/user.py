import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class UserPreferences(BaseModel):
    language: str = "pt-BR"
    date_format: str = "DD/MM/YYYY"
    timezone: str = "America/Sao_Paulo"
    currency_display: str = "BRL"
    onboarding_completed: bool = False


class UserRead(schemas.BaseUser[uuid.UUID]):
    preferences: Optional[dict] = None


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    preferences: Optional[dict] = None
