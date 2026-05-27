from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class AeroportoModel(BaseModel):
    codice: str = Field(..., min_length=3, max_length=3, description="Codice aeroporto (3 caratteri)")
    citta: str = Field(..., min_length=1, description="Città dell'aeroporto")

    @field_validator('codice')
    @classmethod
    def validate_codice(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError('Il codice deve avere solo letteri')
        return v.upper()

    @field_validator('citta')
    @classmethod
    def validate_citta(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('La città non può essere vuota')
        return v.strip().title()


class AeroportoCreate(AeroportoModel):
    pass


class Aeroporto(AeroportoModel):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginateResponse(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int
    data: list[Aeroporto]