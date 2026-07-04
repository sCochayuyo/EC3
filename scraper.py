import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, timeout=15)
driver.get("https://books.toscrape.com/")

wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/aside/div[2]/ul/li/ul/li[18]/a"))).click()

libros = []

while len(libros) < 50:
    elementos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-6.col-sm-4.col-md-3.col-lg-3")))

    for elemento in elementos:
        if len(libros) >= 50:
            break

        try:
            titulo = elemento.find_element(By.XPATH, ".//h3/a").text
            precio = float(elemento.find_element(By.CLASS_NAME, "price_color").replace("£", ""))
            valoracion = elemento.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class").replace("star-rating ", "")
            disponibilidad = elemento.find_element(By.CSS_SELECTOR, ".instock.availability").text
            categoria = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[1]/h1").text
            if valoracion == "one":
                precio = 1
            elif valoracion == "two":
                precio = 2
            elif valoracion == "three":
                precio = 3
            elif valoracion == "four":
                precio = 4
            elif valoracion == "five":
                precio = 5
            libros.append({
                "titulo": titulo,
                "precio": precio,
                "valoracion": valoracion,
                "disponibilidad": disponibilidad,
                "categoria": categoria
            })
            print(f"Guardado: {titulo}")

        except Exception:
            pass
    driver.find_element(By.CLASS_NAME, "next").click()
    time.sleep(2)

driver.quit()