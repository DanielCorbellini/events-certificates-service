from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db import get_db
from models.request_models import CertificateRequest
from services.certificate_service import issue_certificate_service
from repositories.certificado_repository import get_certificate_with_details
import os

router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.post("/emitir")
async def issue_certificate(data: CertificateRequest, db: Session = Depends(get_db)):
    pdf_path = issue_certificate_service(db, data)

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=500, detail="Erro ao gerar certificado")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline"},
        filename="certificado.pdf"
    )


@router.get("/validar/{hash_confirmacao}")
async def validate_and_download(hash_confirmacao: str, db: Session = Depends(get_db)):
    cert = get_certificate_with_details(db, hash_confirmacao)

    if not cert:
        raise HTTPException(
            status_code=404, detail="Certificado não encontrado")

    pdf_path = f"/app/storage/certificados/certificado_{hash_confirmacao}.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404, detail="Arquivo do certificado não encontrado")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"certificado_{hash_confirmacao}.pdf",
        headers={"Content-Disposition": "inline"}
    )


@router.get("/")
async def get_user_certificates():  # user_id e get_event_details()
    pass
