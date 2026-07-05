import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.binary_location = r"C:\Users\Vic3n\AppData\Local\Programs\Opera GX\opera.exe"
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--remote-debugging-port=9222")
service = Service(ChromeDriverManager(driver_version="148.0.7778.265").install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, timeout=15)
driver.get("https://books.toscrape.com/")

wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/aside/div[2]/ul/li/ul/li[18]/a"))).click()

libros = []  # type: ignore[var-annotated]

while len(libros) < 50:
    elementos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-6.col-sm-4.col-md-3.col-lg-3")))

    for elemento in elementos:
        if len(libros) >= 50:
            break

        try:
            titulo = elemento.find_element(By.XPATH, ".//h3/a").text

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

            libros.append({
                "titulo": titulo,
                "precio": precio,
                "valoracion": valoracion,
                "disponibilidad": disponibilidad,
                "categoria": categoria
            })
            print(f"Guardado: {titulo} | Precio: £{precio} | Estrellas: {valoracion}")

        except Exception:
            pass

    # Manejo de paginación con tolerancia a fallos
    try:
        driver.find_element(By.CSS_SELECTOR, ".next a").click()
        time.sleep(2)
    except Exception:
        print("Última página alcanzada.")
        break

driver.quit()