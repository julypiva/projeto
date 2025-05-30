# OBS. pesquisar por "substituir pelo seu" e encontrará os diretórios necessários para mudar!

import pyautogui  # Automação de ações do mouse e teclado
from selenium import webdriver  # Criação do driver do navegador
from selenium.webdriver.common.by import By  # Seleção de elementos (por ID, classe, etc.)
from selenium.webdriver.common.keys import Keys  # Simulação de pressionamento de teclas
from selenium.webdriver.chrome.service import Service  # Gerenciamento do serviço do ChromeDriver
from selenium.webdriver.chrome.options import Options  # Configurações avançadas do navegador Chrome
from selenium.webdriver.support.ui import WebDriverWait  # Espera explícita por elementos na página
from selenium.webdriver.support import expected_conditions as EC  # Condições esperadas para uso com WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  # Execução de ações avançadas (hover, arrastar, etc.)
from datetime import datetime  # Manipulação de datas e horários
import time  # Controle de tempo (ex: sleep)
import pyperclip  # Copiar e colar texto via área de transferência
import os  # Interação com o sistema operacional (ex: arquivos e diretórios)
import pandas as pd  # Manipulação e análise de dados (DataFrames)
import tkinter as tk  # Criação de interfaces gráficas simples
from tkinter import ttk  # Widgets aprimorados do tkinter (ex: botões, labels estilizados)

pyautogui.PAUSE=1 # Respiro de 1 segundo para a pyautogui agir...

def sleep_com_contagem(segundos, mensagem):
    # Configuração da janela da mensagem...
    root = tk.Tk()
    root.overrideredirect(True) 
    largura_janela = 600
    altura_janela = 120
    pos_x = root.winfo_screenwidth() - largura_janela - 50
    pos_y = root.winfo_screenheight() - altura_janela - 50
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.attributes("-topmost", True)

    # Label com quebra de linha e centralização...
    label = ttk.Label(
        root,
        text="",
        font=("Segoe UI Emoji", 14),
        anchor="center",
        justify="center",
        wraplength=largura_janela - 40
    )
    label.pack(expand=True, fill="both", padx=20, pady=20)

    def atualizar_contagem():
        nonlocal segundos
        if segundos > 0:
            label.config(text=f"{mensagem} - Tempo: {segundos} segundos")
            segundos -= 1
            root.after(1000, atualizar_contagem)
        else:
            label.config(text=f"{mensagem} - Tempo: 0 segundos")
            root.after(1000, root.destroy)

    atualizar_contagem()
    root.mainloop()


def iniciar_monitoramento(username, password, perfil):
    driver_path = r"C:\Users\julya.piva\Downloads\chromedriver-win64\chromedriver.exe" # substituir pelo seu
    url = f"https://www.instagram.com/{perfil}/"

    caminho_extensao = r"C:\Users\julya.piva\Downloads\IG_Comment_Export_Tool.crx" # substituir pelo seu

    service = Service(driver_path)
    options = Options()
    options.add_extension(caminho_extensao)  # carregando a extensão do instagram já automaticamente
    options.add_argument("--start-maximized") # maximizando a tela do chrome
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com/") # acessando a página de login do instagram
        sleep_com_contagem(5, "👤 Acessando página de Login do Instagram...")
        pyautogui.hotkey("ctrl", "w") # fechando a página da extensão
        sleep_com_contagem(3, "👤 Fazendo Login...")

        # Fazendo Login...
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        sleep_com_contagem(25, "🚨 Aguarde: digite o código de dois fatores se necessário!")

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
        sleep_com_contagem(8, "✅ Acessando o último post...")
        first_post = driver.find_element(By.XPATH, "//div[@class='_aagw']")
        first_post.click()
        sleep_com_contagem(8, "🔁 Carregando comentários...")

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

        # Espera para garantir que tudo carregou
        sleep_com_contagem(8, "💻 Armazenando URL do Post...")

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
        sleep_com_contagem(8, "🔁 Carregando página...")

        pyautogui.press("tab")
        pyautogui.write(url_temp)
        time.sleep(2)
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        sleep_com_contagem(8, "🔁 Aguardando carregamento...")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        sleep_com_contagem(8, "🔁 Salvando o arquivo xlsx...")

        # TRATAMENTO COM PANDAS
        downloads_path = r"C:\Users\julya.piva\Downloads" # caminho da pasta de downloads (substituir pelo seu)

        # Lista todos os arquivos e pega o mais recente
        files = [os.path.join(downloads_path, f) for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]
        latest_file = max(files, key=os.path.getctime)

        print("Último arquivo baixado:", latest_file)

        # Lê o Excel
        df = pd.read_excel(latest_file)
    
        # Filtra apenas as colunas necesssárias
        df_filtrado = df[['userName', 'text']]

        # Renomeando as colunas...
        df_filtrado = df_filtrado.rename(columns={
            'userName': 'Usuario',
            'text': 'Comentario'
        })

        # Gera nome do arquivo baseado na data/hora atual
        agora = datetime.now().strftime("%d_%m_%Y_%H_%M")
        nome_arquivo = f"comentarios_{agora}.txt"

        # Caminho final de saída
        output_path = os.path.join(r"C:\Users\julya.piva\Desktop\dados\projeto\log comentarios", nome_arquivo) # substituir pelo seu

        # Salva como txt separado por dois-pontos, sem cabeçalho
        df_filtrado.to_csv(output_path, sep=":", index=False, header=False)

        print(f"Arquivo salvo em: {output_path}")
        sleep_com_contagem(5, "✅ Excel com comentários salvo em Downloads...")
        sleep_com_contagem(5, "📉 Iniciar a análise de comentários... Aguarde o retorno na página Home!")

    except Exception as e:
        print(f"Erro geral: {str(e)}")
    finally:
        driver.quit()
