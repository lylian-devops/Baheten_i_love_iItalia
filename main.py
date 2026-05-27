from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
app = FastAPI(
    title="Aeroporti API",
    description="API REST per la gestione degli aeroporti",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi le rotte
app.include_router(router, prefix="/aeroporti", tags=["aeroporti"])

@app.get("/")
def root():
    return {"message": "Aeroporti API - Welcome!", "docs": "/docs"}