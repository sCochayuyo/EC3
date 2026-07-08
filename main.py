from database import create_db
from seed import poblar_base


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

    print("Ejecucion Finalizada")


if __name__ == "__main__":
    main()
