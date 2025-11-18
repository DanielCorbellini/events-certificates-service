from sqlalchemy.orm import Session
from sqlalchemy import text

def get_event_end_date(db: Session, id_evento: int):
    return db.execute(
        text("SELECT data_fim FROM eventos WHERE id_evento = :id"),
        {"id": id_evento}
    ).fetchone()

def get_event_details(db: Session, id_usuario: int):
    return db.execute(
        text("""
            SELECT
                hash_confirmacao,
                data_emissao,
                titulo,
                data_inicio,
                data_fim,
                local
            FROM
                certificados
                LEFT JOIN checkins USING (id_checkin)
                LEFT JOIN inscricoes USING (id_inscricao)
                LEFT JOIN eventos using (id_evento)
            WHERE
                id_usuario = :id"""),
                    {"id": id_usuario}
        ).fetchone()