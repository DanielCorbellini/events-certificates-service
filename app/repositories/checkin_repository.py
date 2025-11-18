from sqlalchemy.orm import Session
from sqlalchemy import text

def get_checkin_by_inscricao(db: Session, id_inscricao: int):
    return db.execute(
        text("SELECT id_checkin FROM checkins WHERE id_inscricao = :id"),
        {"id": id_inscricao}
    ).fetchone()
