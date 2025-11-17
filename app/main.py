from fastapi import FastAPI
from routers import certificates

app = FastAPI(title="Certificado Service")

app.include_router(certificates.router)


@app.middleware("http")
async def db_session_middleware(request, call_next):
    response = await call_next(request)
    return response
