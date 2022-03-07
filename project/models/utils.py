from sqlalchemy import event
from sqlalchemy.engine import Engine

from config import DB

# TODO make sure this still is cascade deleting everything
# tells sqlite3 to accept foreign keys, this is necessary for sqlite3 to be able
# to cascade delete items that have relationships
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(DBapi_connection, connection_record):
    cursor = DBapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def add_to_database(item: object) -> None:
    DB.session.add(item)
    DB.session.commit()


def delete_from_database(item: object) -> None:
    DB.session.delete(item)
    DB.session.commit()
