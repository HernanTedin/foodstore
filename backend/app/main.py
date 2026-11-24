from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine
from app.core.errors import NotFoundError, register_exception_handlers
from app.modules.auth.router import router as auth_router

app = FastAPI(title="Food Store API", version="0.1.0")
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,  # necesario para la cookie HttpOnly
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api/v1")
api.include_router(auth_router)


@api.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}


@api.get("/boom")
def boom():
    raise NotFoundError("Producto no encontrado", field="product_id")


app.include_router(api)
