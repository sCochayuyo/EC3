from typing import Dict, List
from sqlmodel import select
from Models import Categoria, Libro
from database import get_session
from scraper import LibroExtraido


def poblar_base(datos_extraidos: List[LibroExtraido]) -> None:
    """
    Recibe una lista de dataclasses y los guarda en base de datos
    """

    with get_session() as session:
        cache_categorias: Dict[str, Categoria] = {}

        for item in datos_extraidos:

            # Idempotencia de categoria
            if item.categoria not in cache_categorias:
                consulta_categoria = select(Categoria).where(
                    Categoria.nombre == item.categoria
                )
                categoria_existente = session.exec(consulta_categoria).first()

                if not categoria_existente:
                    categoria_existente = Categoria(nombre=item.categoria)
                    session.add(categoria_existente)
                    session.commit()
                    session.refresh(categoria_existente)

                cache_categorias[item.categoria] = categoria_existente

            categoria_actual = cache_categorias[item.categoria]

            # Idempotencia de libro
            consulta_libro = select(Libro).where(Libro.titulo == item.titulo)
            libro_existente = session.exec(consulta_libro).first()

            if not libro_existente:
                esta_disponible = "In stock" in item.disponibilidad

                nuevo_libro = Libro(
                    titulo=item.titulo,
                    precio=item.precio,
                    valoracion=item.valoracion,
                    disponible=esta_disponible,
                    categoria_id=categoria_actual.id,
                    url_detalle=item.url,
                    descripcion=item.descripcion,
                    upc=item.upc
                )
                session.add(nuevo_libro)

        session.commit()
        print("Persistencia finalizada exitosamente.")
