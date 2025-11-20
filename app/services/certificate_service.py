from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from repositories.checkin_repository import get_checkin_by_inscricao
from repositories.evento_repository import get_event_end_date
from repositories.certificado_repository import (
    get_existing_certificate,
    insert_certificate,
    get_certificate_with_details,
    get_user_certificates
)
from utils.certificate_generator import generate_certificate
from services.exceptions import CertificateError
from repositories.inscricao_repository import get_subscription_details


def issue_certificate_service(db: Session, id_inscricao):
    data = get_subscription_details(db, id_inscricao)

    # 1. Validar check-in
    checkin = get_checkin_by_inscricao(db, data.id_inscricao)
    if not checkin:
        raise CertificateError(
            "Usuário não fez check-in para este evento", 400)

    # 2. Validar término do evento
    event = get_event_end_date(db, data.id_evento)
    if not event:
        raise CertificateError("Evento não encontrado", 404)

    event_end = (
        event.data_fim.date()
        if isinstance(event.data_fim, datetime)
        else event.data_fim
    )

    if event_end > datetime.now().date():
        raise CertificateError("Evento ainda não terminou", 400)

    # 3. Verificar se já existe certificado
    exists = get_existing_certificate(db, checkin.id_checkin)
    if exists:
        raise CertificateError(
            "Certificado já emitido para este check-in", 409)

    # 4. Criar hash
    hash_confirmacao = uuid.uuid4().hex

    # 5. Inserir certificado
    new_cert = insert_certificate(db, checkin.id_checkin, hash_confirmacao)
    db.commit()

    # 6. Gerar PDF
    pdf_path = generate_certificate(
        user={"id": data.id_usuario, "name": data.nome},
        event={
            "id": data.id_evento,
            "title": data.titulo,
            "start_date": data.data_inicio,
            "end_date": data.data_fim
        },
        certificate={"id": new_cert.id_certificado, "hash": hash_confirmacao}
    )

    return pdf_path


def get_certification_details(db: Session, hash_confirmacao: str):
    return get_certificate_with_details(db, hash_confirmacao)


def get_user_certifications(db: Session, id_usuario: int):
    return get_user_certificates(db, id_usuario)
