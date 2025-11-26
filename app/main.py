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
async def db_session_middleware(request, call_next):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": "Token não fornecido"}
        )

    token = auth_header.split(" ")[1]

    try:
        # Decodifica e valida o token
        payload = jwt.decode(token, GATEWAY_SECRET, algorithms=[JWT_ALGORITHM])

        # Injeta o JWT no estado da request
        request.state.jwt = payload

    except JWTError as e:
        return JSONResponse(
            status_code=401,
            content={"error": "Token inválido ou expirado", "details": str(e)}
        )
    response = await call_next(request)
    return response


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
