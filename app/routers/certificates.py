from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db import get_db
from models.response_models import CertificateResponse, Certificate, Event
from services.certificate_service import issue_certificate_service, get_user_certifications, get_certification_details
import os


router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.post("/emitir/{id_inscricao}")
async def issue_certificate(id_inscricao: int, db: Session = Depends(get_db)):
    pdf_path = issue_certificate_service(db, id_inscricao)

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
    cert = get_certification_details(db, hash_confirmacao)

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


@router.get("", response_model=CertificateResponse)
async def list_user_certificates(id_usuario: int, db: Session = Depends(get_db)):
    rows = get_user_certifications(db, id_usuario)

    if not rows:
        raise HTTPException(
            status_code=404, detail="Usuário não possui nenhum certificado")

    certificados = [
        Certificate(
            hash_confirmacao=row['hash_confirmacao'],
            data_emissao=row['data_emissao'],
            evento=Event(
                titulo=row['titulo'],
                data_inicio=row['data_inicio'],
                data_fim=row['data_fim'],
                local=row['local']
            )
        ) for row in rows
    ]

    return CertificateResponse(certificados=certificados)
