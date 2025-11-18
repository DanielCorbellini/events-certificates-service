from sqlalchemy.orm import Session
from sqlalchemy import text

def get_existing_certificate(db: Session, id_checkin: int):
    return db.execute(
        text("SELECT id_certificado FROM certificados WHERE id_checkin = :id"),
        {"id": id_checkin}
    ).fetchone()


def insert_certificate(db: Session, id_checkin: int, hash_confirmacao: str):
    return db.execute(
        text("""
            INSERT INTO certificados (id_checkin, hash_confirmacao)
            VALUES (:id_checkin, :hash)
            RETURNING id_certificado
        """),
        {"id_checkin": id_checkin, "hash": hash_confirmacao}
    ).fetchone()


def get_certificate_with_details(db: Session, hash_confirmacao: str):
    return db.execute(
        text("""
            SELECT c.id_certificado, c.id_checkin, c.data_emissao,
                   c.hash_confirmacao, i.id_usuario, i.id_evento
            FROM certificados c
            JOIN checkins ch ON ch.id_checkin = c.id_checkin
            JOIN inscricoes i ON i.id_inscricao = ch.id_inscricao
            WHERE c.hash_confirmacao = :hash
        """),
        {"hash": hash_confirmacao}
    ).fetchone()
