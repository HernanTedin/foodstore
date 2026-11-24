# Food Store

Trabajo Final Integrador · Programación 3 + Arquitectura y Diseño de Interfaces.
Tienda de comidas con catálogo, pedidos, pagos e inventario. Proyecto individual.

## Stack

- **Backend:** FastAPI, SQLModel, Alembic, PostgreSQL 16, bcrypt, JWT en cookie HttpOnly
- **Frontend:** React 19, TypeScript, Vite, Tailwind 4, TanStack Query, Zustand, React Router
- **Infraestructura:** Docker (PostgreSQL)

## Requisitos

- Python 3.12 o superior
- Node.js 20 o superior
- Docker Desktop (abierto y corriendo)
- Git

## Cómo correrlo (Windows, PowerShell)

Todos los comandos se ejecutan desde la carpeta raíz del proyecto, salvo que se indique otra.

### 1. Base de datos

```powershell
docker compose up -d
```

### 2. Backend

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
cd backend
copy .env.example .env
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

En el archivo `backend\.env` conviene reemplazar `SECRET_KEY` por una clave propia de al menos 32 caracteres.

### 3. Frontend (en otra terminal, desde la raíz)

```powershell
cd frontend
npm install
npm run dev
```

## Direcciones

| Qué | URL |
|---|---|
| Aplicación | http://localhost:5173 |
| API (Swagger) | http://localhost:8000/docs |
| Estado del servidor | http://localhost:8000/api/v1/health |

## Usuario administrador

Lo crea el seed: `admin@foodstore.com` / `FoodStore2026!` (solo para desarrollo).

## Estructura

- `backend/` · API en capas (router, service, unit of work, repository) organizada por módulos.
- `frontend/` · aplicación React organizada por features.
- `docker-compose.yml` · base de datos PostgreSQL.
- `docs/` · documentación del proyecto.

## Estado del proyecto

Fase 0 (fundamentos) completa: estructura, entornos, arquitectura base, seguridad, autenticación, las 26 tablas migradas, seed y pantallas de acceso. Próxima fase: administración de usuarios.