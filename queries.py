from sqlmodel import Session, func, select
from models import Categoria, Libro


def total_items(session: Session) -> int:
    """
    Retorna el numero total de libros almacenados en la base de datos.
    """

    consulta = select(func.count()).select_from(Libro)
    total = session.exec(consulta).one()

    return total


def items_por_categoria(session: Session) -> list[tuple[str, int]]:
    """
    Retorna cada categoria y la cantidad de libros que contiene,
    ordenado de mayor a menor
    """
    consulta = (
        select(Categoria.nombre, func.count())
        .join(Libro)
        .group_by(Categoria.nombre)
        .order_by(func.count().desc())
    )

    resultado = session.exec(consulta).all()

    return [(nombre, cantidad) for nombre, cantidad in resultado]
