from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional
from .database import db
from .schemas import AeroportoCreate, AeroportoModel, PaginatedResponse
from .auth import verify_api_key
router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def get_aeroporti(
        page: int = Query(1, ge=1, description="Numero pagina"),
        size: int = Query(5, ge=1, le=100, description="Elementi per pagina")
):
    """
    Restituisce la lista degli aeroporti con paginazione
    """
    aeroporti, total = db.get_all(page, size)
    total_pages = (total + size - 1) // size if total > 0 else 0

    return PaginatedResponse(
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
        data=aeroporti
    )

@router.get("/{aeroporto_id}", response_model=Aeroporto)
def get_aeroporto(aeroporto_id: int):
    """
    Restituisce un aeroporto specifico tramite ID
    """
    aeroporto = db.get_by_id(aeroporto_id)
    if not aeroporto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto con ID {aeroporto_id} non trovato"
        )
    return aeroporto


@router.post("/", response_model=Aeroporto, status_code=status.HTTP_201_CREATED)
def create_aeroporto(
        aeroporto: AeroportoCreate,
        api_key: str = Depends(verify_api_key)
):
    """
    Crea un nuovo aeroporto (protetto da API Key)
    """
    try:
        new_aeroporto = db.create(aeroporto)
        return new_aeroporto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{aeroporto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aeroporto(
        aeroporto_id: int,
        api_key: str = Depends(verify_api_key)
):

    deleted = db.delete(aeroporto_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto con ID {aeroporto_id} non trovato"
        )
    return None


# Endpoint opzionale per PUT (update)
@router.put("/{aeroporto_id}", response_model=Aeroporto)
def update_aeroporto(
        aeroporto_id: int,
        aeroporto: AeroportoCreate,
        api_key: str = Depends(verify_api_key)
):

    try:
        updated = db.update(aeroporto_id, aeroporto)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aeroporto con ID {aeroporto_id} non trovato"
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail=str(a)
        )