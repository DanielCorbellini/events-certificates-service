from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import certificates
from services.exceptions import CertificateError
from jose import jwt, JWTError
import os

app = FastAPI(title="Certificado Service")

app.include_router(certificates.router)

GATEWAY_SECRET = os.getenv("GATEWAY_SECRET")
JWT_ALGORITHM = "HS256"


@app.middleware("http")
async def gateway_key_middleware(request: Request, call_next):
    gateway_key = request.headers.get("X-Gateway-Key")

    if gateway_key is None or gateway_key != GATEWAY_SECRET:
        return JSONResponse(
            status_code=403,
            content={"error": "Acesso negado"}
        )

    return await call_next(request)


@app.exception_handler(CertificateError)
async def certificate_exception_handler(request: Request, exc: CertificateError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )
