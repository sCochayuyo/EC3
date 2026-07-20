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
        print("\nConsulta 1 Total de libros:")
        total_libros = queries.total_items(session)
        print(f"Total de libros en base de datos: {total_libros}")

        print("\nConsulta 2 libros por categoria:")
        agrupacion_cat = queries.items_por_categoria(session)
        for categoria, cantidad in agrupacion_cat:
            print(f"- {categoria}: {cantidad} libros")

        print("\n Consulta 3 Top 10 Libros (por valoracion):")
        top_10 = queries.top_10_por_criterio(session)
        for i, (titulo, valoracion) in enumerate(top_10, start=1):
            print(f"{i}. {titulo} Valoracion:{valoracion}")
        print()

        print("Consulta 4 Estadisticas de Precios por Categoria:")
        stats = queries.estadisticas(session)
        for categoria, datos in stats.items():
            print(f"Categoría: {categoria}")
            print(f"  - Promedio: ${datos['promedio']:.2f}")
            print(f"  - Máximo: ${datos['maximo']}")
            print(f"  - Mínimo: ${datos['minimo']}")

    print("\nEjecucion Finalizada")


if __name__ == "__main__":
    main()
