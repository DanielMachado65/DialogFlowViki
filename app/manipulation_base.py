import sqlite3

from app.models.models import RequestUser

connection = sqlite3.connect('base.db')
c = connection.cursor()

c.execute("""
    create table request(
        session text,
        name text,
        id integer,
        texto text,
        timestamp text
    )
""")


def insert_request(request):
    with c:
        c.execute("insert into requerst(:session, :name, :id, :texto, :timestamp",{
            "session": request.session,
            "name": request.name,
            "id": request.id,
            "texto": request.texto,
            "timestamp": request.timestamp
        })
