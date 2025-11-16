from fastapi import APIRouter
from fastapi.responses import FileResponse
from models.request_models import CertificateRequest
from services.certificate_generator import generate_certificate

router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.post("/emitir")
async def issue_certificate(data: CertificateRequest):
    # Validar se o usuário fez checkin e está realmente naquele evento

    pdf_path = generate_certificate(
        user={
            "id": data.id_usuario,
            "name": data.nome
        }, event={
            "id": data.id_evento,
            "title": data.titulo,
            "start_date": data.data_inicio,
            "end_date": data.data_fim
        }
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="certificado.pdf"
    )


@router.post("/validar")
async def validate_certificate():
    pass
