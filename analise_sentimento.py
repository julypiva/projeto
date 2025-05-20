import os
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

analyzer = SentimentIntensityAnalyzer()

# Caminhos dos dicionários
CAMINHO_DICIONARIOS = r"C:\Users\julya.piva\Desktop\dados\projeto"
elogios = set()
ofensas = set()

# Carrega os dicionários personalizados
def carregar_dicionarios():
    global elogios, ofensas
    with open(os.path.join(CAMINHO_DICIONARIOS, "dicionario_elogios.txt"), "r", encoding="utf-8") as f:
        elogios = set([linha.strip().lower() for linha in f if linha.strip()])
    with open(os.path.join(CAMINHO_DICIONARIOS, "dicionario_ofensas.txt"), "r", encoding="utf-8") as f:
        ofensas = set([linha.strip().lower() for linha in f if linha.strip()])

# Função de análise com VADER + tradução + dicionários

def analisar_sentimento_vader(texto_pt):
    if not texto_pt or not texto_pt.strip():
        return "Comentário vazio"

    try:
        texto_en = GoogleTranslator(source='pt', target='en').translate(texto_pt)
    except:
        texto_en = texto_pt  # fallback se falhar a tradução

    if not texto_en or not texto_en.strip():
        return "Comentário inválido"

    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(texto_en)

    if score['compound'] >= 0.05:
        sentimento = "Positivo"
    elif score['compound'] <= -0.05:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    # Refinamento com dicionários
    palavras = set(texto_pt.lower().split())
    if sentimento == "Neutro":
        if palavras & elogios:
            sentimento = "Positivo"
        elif palavras & ofensas:
            sentimento = "Negativo"

    return sentimento

# Processamento completo dos comentários
def processar_analise_sentimento():
    carregar_dicionarios()

    pasta_comentarios = r"C:\Users\julya.piva\Desktop\dados\projeto\log comentarios"
    arquivos = [f for f in os.listdir(pasta_comentarios) if f.endswith(".txt")]
    caminho_arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(os.path.join(pasta_comentarios, f)))
    caminho_arquivo = os.path.join(pasta_comentarios, caminho_arquivo_mais_recente)
    
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    resultados = []
    for linha in linhas:
        try:
            usuario, comentario = linha.split(":", 1)
            sentimento = analisar_sentimento_vader(comentario.strip())
            resultados.append({
                "usuario": usuario.strip() if usuario.strip() else "Usuário não identificado",
                "comentario": comentario.strip() if comentario.strip() else "Comentário não encontrado",
                "sentimento": sentimento
            })
        except ValueError:
            continue

    # Salva o resultado em arquivo
    data_atual = datetime.now().strftime("%d_%m_%Y_%H_%M")
    nome_arquivo = f"analise_sentimento_{data_atual}.txt"
    caminho_arquivo_resultado = os.path.join(r"C:\Users\julya.piva\Desktop\dados\projeto\log_analise", nome_arquivo)

    with open(caminho_arquivo_resultado, "w", encoding="utf-8") as f:
        for resultado in resultados:
            f.write(f"Usuário: {resultado['usuario']}\n")
            f.write(f"Comentário: {resultado['comentario']}\n")
            f.write(f"Sentimento: {resultado['sentimento']}\n\n")

    return resultados

