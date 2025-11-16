from fastapi import FastAPI
from routers import certificates

app = FastAPI(title="Certificado Service")

app.include_router(certificates.router)
