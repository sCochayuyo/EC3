from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Categoria(SQLModel, table=True):
    """
    Entidad que representa la categoria tematica.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)

    Libros: List["Libro"] = Relationship(back_populates="Categoria")


class Libro(SQLModel, table=True):

    """
    Entidad que representa un libro extraido del sitio web con sus detalles.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    precio: float
    valoracion: int
    disponible: bool
    categoria_id: int = Field(foreign_key="categoria.id")
    url_detalle: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    upc: Optional[str] = Field(default=None)

    categoria: Optional["Categoria"] = Relationship(back_populates="libros")
