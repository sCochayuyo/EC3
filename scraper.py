import time
from dataclasses import dataclass
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class LibroExtraido:
    titulo: str
    url: str
    precio: float
    valoracion: int
    disponibilidad: str
    categoria: str
    upc: Optional[str] = None
    descripcion: Optional[str] = None


options = Options()

# Configuracion Opera
# options.binary_location = r"C:\Users\Vic3n\AppData\Local\Programs\Opera GX\opera.exe"
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")
# options.add_argument("--remote-debugging-port=9222")
# service = Service(ChromeDriverManager(driver_version="148.0.7778.265").install())
# driver = webdriver.Chrome(service=service, options=options)

# Configuracion Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


wait = WebDriverWait(driver, timeout=15)
driver.get("https://books.toscrape.com/")

wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/aside/div[2]/ul/li/ul/li[18]/a"))).click()

libros: list[LibroExtraido] = []
i = 0

while len(libros) < 50:
    elementos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-6.col-sm-4.col-md-3.col-lg-3")))

    for elemento in elementos:
        if len(libros) >= 50:
            break

        try:

            i += 1
            titulo = elemento.find_element(By.XPATH, ".//h3/a").text

            url_libro = elemento.find_element(By.XPATH, ".//h3/a").get_attribute("href")

            # Limpieza del precio requerida para guardarlo como float
            precio_texto = elemento.find_element(By.CLASS_NAME, "price_color").text.replace("£", "")
            precio = float(precio_texto)

            valoracion_texto = elemento.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class").replace("star-rating ", "")  # type: ignore[union-attr]
            disponibilidad = elemento.find_element(By.CSS_SELECTOR, ".instock.availability").text
            categoria = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[1]/h1").text

            # Asignación correcta de la variable 'valoracion'
            valoracion = 0
            if valoracion_texto == "One":
                valoracion = 1
            elif valoracion_texto == "Two":
                valoracion = 2
            elif valoracion_texto == "Three":
                valoracion = 3
            elif valoracion_texto == "Four":
                valoracion = 4
            elif valoracion_texto == "Five":
                valoracion = 5

            nuevo_libro = LibroExtraido(
                titulo=titulo,
                url=str(url_libro),
                precio=precio,
                valoracion=valoracion,
                disponibilidad=disponibilidad,
                categoria=categoria
            )
            libros.append(nuevo_libro)
            print(f" {i} | Titulo: {titulo} | Precio: £{precio}  | Estrellas: {valoracion} | Disponibilidad: {disponibilidad} | Categoria: {categoria}")

        except Exception:
            pass

    # Manejo de paginación con tolerancia a fallos
    try:
        driver.find_element(By.CSS_SELECTOR, ".next a").click()
        time.sleep(2)
    except Exception:
        print("Última página alcanzada.")
        break

# Obtencion de campos adicionales
for index, libro in enumerate(libros):
    try:
        driver.get(libro.url)

        try:
            libro.upc = driver.find_element(
                By.XPATH, "//th[text()='UPC']/following-sibling::td"
            ).text
        except Exception:
            libro.upc = "N/A"

        try:
            libro.descripcion = driver.find_element(
                By.XPATH,
                "//div[@id='product_description']/following-sibling::p"
            ).text
        except Exception:
            libro.descripcion = "Sin descripción"

    except Exception as e:
        print(f"Error accediendo a los detalles de '{libro.titulo}': {e}")


driver.quit()
