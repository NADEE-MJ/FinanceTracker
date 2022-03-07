from config import DB


def add_to_database(item: object) -> None:
    DB.session.add(item)
    DB.session.commit()


def delete_from_database(item: object) -> None:
    DB.session.delete(item)
    DB.session.commit()
