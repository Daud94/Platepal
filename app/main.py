import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import auth
from app.config import settings
from app.database import create_db_and_tables

app = FastAPI(
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


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
