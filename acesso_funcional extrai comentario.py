from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime

# caminho do chromedriver 
driver_path = r"C:\\Users\\julya.piva\\Downloads\\chromedriver-win64\\chromedriver.exe"

username = "julypivaa" # seu login do instagram para acesso
password = "Minhasenha" # sua senha do instagram

# URL do Instagram que queremos visitar
url = "https://www.instagram.com/isapagels/"

# iniciando o chrome driver...
service = Service(driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

def login_instagram():
    driver.get("https://www.instagram.com/") # acessando link do instagram
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username") # selecionando campo de usuário
    username_input.send_keys(username) # preenchendo usuário

    password_input = driver.find_element(By.NAME, "password") # selecionando campo de senha
    password_input.send_keys(password) # preenchendo usuário
    password_input.send_keys(Keys.RETURN)

    time.sleep(45) # espera a página carregar, ou preencha seu token de autenticação de 2 fatores
    print("carregou a página... espera mais 5 segundos")
    time.sleep(5)

    # Validação para o caso de telas dinâmicas...
    try:
        driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
    except:
        pass

    try:
        driver.find_element(By.XPATH, "//button[text()='Agora não']").click()
    except:
        pass

# Coletando os comentários
def collect_comments(): 
    driver.get(url) # acessando link do perfil que queremos visitar
    time.sleep(35)

    first_post = driver.find_element(By.XPATH, "//div[@class='_aagw']") # acessando ao último post da página
    first_post.click() 
    time.sleep(15)

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 500);") # captando toda a tela de comentários
        time.sleep(2)

    # Armazenando os comentários...
    comments = []
    comment_elements = driver.find_elements(By.XPATH, "//li[contains(@class, '_a9zj')]")

    # Criando condições para comentários não encontrados ou usuários não identificados...
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

    # Definindo variável de datas e caminho das pastas...
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
    folder_path = r"C:\Users\julya.piva\Desktop\projeto\log_comentarios"
    file_path = folder_path + f"\\comentarios_{current_time}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for comment in comments:
            file.write(comment + "\n")
    print(f"Comentários armazenados em '{file_path}'.")

def ler_arquivos_salvos():
    print("\n--- Lendo arquivos na pasta (sem os.listdir) ---")
    
    # Lista de nomes padrão dos arquivos já salvos...
    nomes_arquivos = [
        "comentarios_28_04_2025_15_30.txt",
        "comentarios_28_04_2025_15_50.txt",
        "comentarios_28_04_2025_16_10.txt"
    ]
    
    pasta = r"C:\Users\julya.piva\Desktop\projeto\log_comentarios"

    # Percorre a lista de arquivos definidos anteriormente
    for nome in nomes_arquivos:
        
        # Monta o caminho completo do arquivo juntando a pasta e o nome 
        caminho = pasta + "\\" + nome

        # Printa o arquivo que ele encontrou 
        print(f"\nLendo arquivo: {caminho}")

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                # Lê todo o conteúdo do arquivo
                conteudo = f.read()
                print(conteudo)

        # Print para saber se encontramos o arquivo...
        except FileNotFoundError:
            print(f"Arquivo '{nome}' não encontrado.")

        # Pegando algum possível erro ao ler o arquivo...
        except Exception as e:
            print(f"Erro ao abrir '{nome}': {e}")

# Execução da def
try:
    login_instagram()
    collect_comments()
    ler_arquivos_salvos()
finally:
    time.sleep(40)
    driver.quit()
