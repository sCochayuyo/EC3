from database import create_db, get_session
from seed import poblar_base
import queries


def main() -> None:
    """
    Inicializa BD, ejecuta scraper y persiste datos
    """
    print("1.- Inicializando Base de Datos")
    create_db()

    print("2.- Comenzando Extraccion web")
    import scraper

    print("3.- Guardando datos")
    poblar_base(scraper.libros)

    print("4.- Ejecucion de Consultas")
    with get_session() as session:
        print("\nConsulta 1:")
        total_libros = queries.total_items(session)
        print(f"Total de libros en base de datos: {total_libros}")

        print("\nConsulta 2:")
        agrupacion_cat = queries.items_por_categoria(session)
        for categoria, cantidad in agrupacion_cat:
            print(f"- {categoria}: {cantidad} libros")

    print("\nEjecucion Finalizada")


if __name__ == "__main__":
    main()
