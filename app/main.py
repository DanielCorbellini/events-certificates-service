from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import certificates
from services.exceptions import CertificateError

app = FastAPI(title="Certificado Service")

app.include_router(certificates.router)


@app.middleware("http")
async def db_session_middleware(request, call_next):
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
