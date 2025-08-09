from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from rich import print, panel

from app.config.database import create_db_and_tables
from app.config.env_config import settings
from app.router import router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Starting up...", border_style="green"))
    await create_db_and_tables()
    yield
    print(panel.Panel("Shutting down...", border_style="red"))
app = FastAPI(
    lifespan=lifespan_handler,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Custom exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "success": False}
    )

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


app.include_router(router)
