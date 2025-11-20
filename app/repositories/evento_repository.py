from sqlalchemy.orm import Session
from sqlalchemy import text


def get_event_end_date(db: Session, id_evento: int):
    return db.execute(
        text("SELECT data_fim FROM eventos WHERE id_evento = :id"),
        {"id": id_evento}
    ).fetchone()
