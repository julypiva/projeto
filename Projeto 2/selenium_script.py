from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import os

def iniciar_monitoramento(username, password, perfil):
    driver_path = r"C:\\Users\\ISABELLYCONSTANTINOP\\Downloads\\chromedriver-win64\\chromedriver.exe"
    url = f"https://www.instagram.com/{perfil}/"

    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(45)

        try:
            driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
        except:
            pass
        try:
            driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
        except:
            pass

        driver.get(url)
        time.sleep(35)

        driver.find_element(By.XPATH, "//div[@class='_aagw']").click()
        time.sleep(15)

        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)

        comments = []
        comment_elements = driver.find_elements(By.XPATH, "//li[contains(@class, '_a9zj')]")

        for comment in comment_elements:
            try:
                user = comment.find_element(By.XPATH, ".//h3//a").text
            except:
                try:
                    user = comment.find_element(By.XPATH, ".//h3//span").text
                except:
                    user = "Usuário não identificado"

            try:
                text = comment.find_element(By.XPATH, ".//span[contains(@class, '_ap3a')]").text
            except:
                text = "Comentário não encontrado"

            comments.append(f"{user}: {text}")

        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
        folder_path = r"C:\Users\ISABELLYCONSTANTINOP\Desktop\Projeto 2\log comentarios"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"comentarios_{current_time}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            for comment in comments:
                file.write(comment + "\n")

        return f"Comentários armazenados em '{file_path}'."

    except Exception as e:
        return f"Erro: {str(e)}"
    finally:
        time.sleep(10)
        driver.quit()
