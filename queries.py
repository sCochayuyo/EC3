from sqlmodel import Session, select, func, col, case, text
from models import Categoria, Libro

from EC3.Models import Libro, Categoria


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

def top_10_por_criterio(session: Session) -> list:
    consulta =(
        select(Libro.titulo)
        .order_by(col(Libro.valoracion).desc()).limit(10)
    )
    resultado = session.exec(consulta).all()

    return list(resultado)

def estadisticas(session: Session) -> dict:
    consulta = (
        select(Categoria.nombre, func.avg(Libro.precio), func.max(Libro.precio), func.min(Libro.precio))
        .join(Categoria)
        .group_by(Categoria.nombre)
    )
    resultados = session.exec(consulta).all()
    grupos = {}
    for resultado in resultados:
        categoria = resultado[0]
        grupos[categoria] = {
            "promedio": float(resultado[1]),
            "maximo": resultado[2],
            "minimo": resultado[3]
        }
    return grupos