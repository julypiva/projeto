from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os
from datetime import datetime

# caminho do chromedriver
driver_path = r"C:\\Users\\julya.piva\\Downloads\\chromedriver-win64\\chromedriver.exe"

# aqui você precisa ajustar conforme suas credenciais do Instagram...
username = "seu_user" 
password = "sua_senha"

# URL do Instagram, aqui você também pode ajustar conforme o perfil que você gostaria de visitar!
url = "https://www.instagram.com/isapagels/"

# iniciando o driver
service = Service(driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window() # comando para maximizar a tela do chrome quando abrir...

def login_instagram():
    driver.get("https://www.instagram.com/") # acessando instagram...
    time.sleep(5)

    # insere o nome de usuário
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)

    # insere a senha
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    # pressiona o Enter pra fazer login
    password_input.send_keys(Keys.RETURN)
    time.sleep(40)  # esperar a pagina carregar
    print("carregou a página... espera mais 10 segundos")
    time.sleep(1000000)

    # fechar popups
    try:
        driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
    except:
        pass

    try:
        driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
    except:
        pass

# aqui começamos a coletar os comentarios...
def collect_comments():
    driver.get(url)
    time.sleep(15)

    # clica no último post
    first_post = driver.find_element(By.XPATH, "//div[@class='_aagw']")  
    first_post.click()
    time.sleep(10)

    # rola a tela para carregar mais comentários
    for _ in range(5):  
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

    # pegando os comentários...
    comments = []
    comment_elements = driver.find_elements(By.XPATH, "//li[contains(@class, '_a9zj')]")

    for comment in comment_elements:
        try:
            # primeiro tenta pegar o nome do usuário normalmente
            user = comment.find_element(By.XPATH, ".//h3//a").text
        except:
            # se não encontrar no <a>, tenta pegar dentro de um <span>
            try:
                user = comment.find_element(By.XPATH, ".//h3//span").text
            except:
                user = "Usuário não identificado"  # se falhar, define um nome genérico

        try:
            text = comment.find_element(By.XPATH, ".//span[contains(@class, '_ap3a')]").text
        except:
            text = "Comentário não encontrado"  # se falhar, define um texto genérico

        comments.append(f"{user}: {text}")

    # gerar nome do arquivo com data e hora
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
    folder_path = r"C:\Users\julya.piva\Desktop\projeto\log_comentarios"
    
    # cria a pasta se não existir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, f"comentarios_{current_time}.txt")

    # armazenar os comentários em um arquivo txt
    with open(file_path, "w", encoding="utf-8") as file:
        for comment in comments:
            file.write(comment + "\n")
    print(f"Comentários armazenados em '{file_path}'.")

# execução
try:
    login_instagram()  # fazer login
    collect_comments()  # coletar e armazenar comentários
finally:
    time.sleep(10000)
    driver.quit()  # fechar o navegador ao final
