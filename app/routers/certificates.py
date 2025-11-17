from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import uuid
from db import get_db
from models.request_models import CertificateRequest
from services.certificate_generator import generate_certificate

router = APIRouter(prefix="/certificados", tags=["Certificados"])

"""
O que fazer
1. Inserir certificado no banco
2. Recuperar o certificado com o validar (salvar o caminho no banco)
3. Url para download

"""


@router.post("/emitir")
async def issue_certificate(data: CertificateRequest, db: Session = Depends(get_db)):
    # 1. Validar check-in
    checkin = db.execute(
        text("SELECT id_checkin FROM checkins WHERE id_inscricao = :id_inscricao"),
        {"id_inscricao": data.id_inscricao}
    ).fetchone()

    if not checkin:
        raise HTTPException(
            status_code=400, detail="Usuário não fez check-in para este evento")

    # 2. Verificar se evento já terminou
    db_event = db.execute(
        text("SELECT data_fim FROM eventos WHERE id_evento = :id_evento"),
        {"id_evento": data.id_evento}
    ).fetchone()

    if not db_event:
        raise HTTPException(status_code=400, detail="Evento não encontrado")

    # db_event.data_fim vem como date/datetime do SQLAlchemy
    if db_event.data_fim > datetime.now().date():
        raise HTTPException(
            status_code=400, detail="Evento ainda não terminou")

    # 3. Checar se já existe certificado
    existing = db.execute(
        text("SELECT id_certificado FROM certificados WHERE id_checkin = :id_checkin"),
        {"id_checkin": checkin.id_checkin}
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=400, detail="Certificado já emitido para este check-in")

    # 4. Criar hash único
    hash_confirmacao = uuid.uuid4().hex

    # 5. Inserir o certificado no banco
    new_cert = db.execute(
        text("""
            INSERT INTO certificados (id_checkin, hash_confirmacao)
            VALUES (:id_checkin, :hash)
            RETURNING id_certificado
        """),
        {"id_checkin": checkin.id_checkin, "hash": hash_confirmacao}
    ).fetchone()

    db.commit()

    # 6. Gerar o PDF
    pdf_path = generate_certificate(
        user={
            "id": data.id_usuario,
            "name": data.nome
        },
        event={
            "id": data.id_evento,
            "title": data.titulo,
            "start_date": data.data_inicio,
            "end_date": data.data_fim
        },
        certificate={
            "id": new_cert.id_certificado,
            "hash": hash_confirmacao
        }
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="certificado.pdf"
    )


@router.get("/validar/{hash_confirmacao}")
async def validate_certificate(hash_confirmacao: str, db: Session = Depends(get_db)):
    """
    Valida um certificado pelo hash único público
    """
    certificate = db.execute(
        text("SELECT c.id_certificado, c.id_checkin, c.data_emissao, c.hash_confirmacao, "
             "i.id_usuario, i.id_evento "
             "FROM certificados c "
             "JOIN checkins ch ON ch.id_checkin = c.id_checkin "
             "JOIN inscricoes i ON i.id_inscricao = ch.id_inscricao "
             "WHERE c.hash_confirmacao = :hash"),
        {"hash": hash_confirmacao}
    ).fetchone()

    if not certificate:
        raise HTTPException(
            status_code=404, detail="Certificado não encontrado")

    return {
        "status": "ok",
        "certificado": {
            "id_certificado": certificate.id_certificado,
            "id_checkin": certificate.id_checkin,
            "data_emissao": certificate.data_emissao,
            "hash_confirmacao": certificate.hash_confirmacao,
            "id_usuario": certificate.id_usuario,
            "id_evento": certificate.id_evento
        }
    }
