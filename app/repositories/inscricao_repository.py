from sqlalchemy.orm import Session
from sqlalchemy import text


def get_subscription_details(db: Session, id_inscricao: int):
    return db.execute(
        text("""
            SELECT
                id_usuario,
                nome,
                id_evento,
                id_inscricao,
                titulo,
                data_inicio,
                data_fim
            FROM
                inscricoes
                LEFT JOIN usuarios USING (id_usuario)
                LEFT JOIN eventos USING (id_evento)
            WHERE id_inscricao = :id"""),
        {"id": id_inscricao}
    ).fetchone()
