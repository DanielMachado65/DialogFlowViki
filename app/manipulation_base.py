import sqlite3 as sql

connection_bank = sql.connect('base.db')
connection = connection_bank.cursor()


def create_table(connection):
    connection.execute("""create table request(
        session text,
        name text,
        id integer,
        texto text,
        timestamp text)""")


def insert_request(request):
    with connection:
        connection.execute("insert into requerst(:session, :name, :id, :texto, :timestamp", {
            "session": request.session,
            "name": request.name,
            "id": request.id,
            "texto": request.texto,
            "timestamp": request.timestamp
        })


def get_request_id(connection, id):
    with connection:
        connection.execute("select * from request where id = :id", {
            "id": id
        })
        return connection.fetchall()


def get_all_request(connection):
    with connection:
        connection.execute("select * from request ")
        return connection.fetchall()
