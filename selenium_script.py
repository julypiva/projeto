import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import pyperclip
import os
import pandas as pd

pyautogui.PAUSE=1

def iniciar_monitoramento(username, password, perfil):
    driver_path = r"C:\Users\julya.piva\Downloads\chromedriver-win64\chromedriver.exe"
    url = f"https://www.instagram.com/{perfil}/"

    caminho_extensao = r"C:\Users\julya.piva\Downloads\IG_Comment_Export_Tool.crx"

    service = Service(driver_path)
    options = Options()
    options.add_extension(caminho_extensao)  # 👉 aqui carrega a extensão automaticamente
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        # Login
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        print("🚨 Aguarde: digite o código de dois fatores manualmente no navegador.")
        time.sleep(25)

        # Clicar nos botões "Agora não", se aparecerem
        for _ in range(2):
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Agora não']"))
                ).click()
            except:
                pass

        # Acessar o perfil
        driver.get(url)
        time.sleep(8)
        first_post = driver.find_element(By.XPATH, "//div[@class='_aagw']")
        first_post.click()
        print("✅ Entrou no último post.")
        time.sleep(8)

        # Esperar botão "Mais opções"
        wait = WebDriverWait(driver, 10)
        botao_mais_opcoes = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Mais opções"]'))
        )
        ActionChains(driver).move_to_element(botao_mais_opcoes).click().perform()

        # Clicar em "Ir para a publicação"
        try:
            ir_publicacao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Ir para a publicação"]'))
            )
            ir_publicacao.click()
            print("➡️ Clicou em 'Ir para a publicação'.")
        except Exception as e:
            print("❌ Erro ao clicar em 'Ir para a publicação':", e)

        from bs4 import BeautifulSoup

        # Espera para garantir que tudo carregou
        time.sleep(8)

        # Coletando Comentários com base na url
        pyautogui.hotkey('ctrl', 'l') # acessa a barra de pesquisa
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c') # copia a URL
        time.sleep(2)

        # Armazenar a URL copiada em uma variável
        url_temp = pyperclip.paste()
        print("URL atual:", url_temp)

        time.sleep(2)
        pyautogui.hotkey("ctrl", "t")
        time.sleep(4)
        pyautogui.write("chrome-extension://hpfnaodfcakdfbnompnfglhjmkoinbfm/options.html")
        pyautogui.press("enter")
        time.sleep(8)  # espera o carregamento

        pyautogui.press("tab")
        pyautogui.write(url_temp)
        time.sleep(2)
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        time.sleep(250)
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        time.sleep(15) #salvando o arquivo

        # TRATAMENTO COM PANDAS
        downloads_path = r"C:\Users\julya.piva\Downloads" # caminho da pasta de downloads 

        # Lista todos os arquivos e pega o mais recente
        files = [os.path.join(downloads_path, f) for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]
        latest_file = max(files, key=os.path.getctime)

        print("Último arquivo baixado:", latest_file)

        # Lê o Excel
        df = pd.read_excel(latest_file)
    
        # Filtra apenas as colunas desejadas
        df_filtrado = df[['userName', 'text']]

        # Renomeando as colunas...
        df_filtrado = df_filtrado.rename(columns={
            'userName': 'Usuario',
            'text': 'Comentario'
        })

        # Gera nome do arquivo baseado na data/hora atual
        # Gera nome do arquivo baseado na data/hora atual
        agora = datetime.now().strftime("%d_%m_%Y_%H_%M")
        nome_arquivo = f"comentarios_{agora}.txt"

        # Caminho final de saída
        output_path = os.path.join(r"C:\Users\julya.piva\Desktop\dados\projeto\log comentarios", nome_arquivo)

        # Salva como txt separado por dois-pontos, sem cabeçalho
        df_filtrado.to_csv(output_path, sep=":", index=False, header=False)

        print(f"Arquivo salvo em: {output_path}")
        time.sleep(10)

    except Exception as e:
        print(f"Erro geral: {str(e)}")
    finally:
        driver.quit()