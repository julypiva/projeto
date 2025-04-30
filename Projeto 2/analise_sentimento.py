from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import os

# Baixando os dados necessários do VADER
nltk.download('vader_lexicon')

# Inicializar o analisador de sentimentos VADER
sia = SentimentIntensityAnalyzer()

# Personalizando o lexicon do VADER para português
custom_words = {
    "odeio": -3.0, "feia": -2.5, "nojento": -3.0,
    "péssimo": -3.5, "detesto": -3.0, "ridículo": -2.8, "horrível": -3.0,
    "maravilhoso": 3.5, "incrível": 3.0, "perfeito": 3.5, "adoro": 2.8
}
sia.lexicon.update(custom_words)

# Função para analisar o sentimento
def analisar_sentimento(texto):
    scores = sia.polarity_scores(texto)
    polaridade = scores['compound']  # Valor composto para determinar o sentimento
    return "Positivo" if polaridade > 0.05 else "Negativo" if polaridade < -0.05 else "Neutro"

# Função principal para processar e retornar os resultados da análise de sentimentos
def processar_analise_sentimento():
    pasta_comentarios = r"C:\Users\ISABELLYCONSTANTINOP\Desktop\Projeto 2\log comentarios"
    
    # Encontrando o arquivo mais recente na pasta de comentários
    arquivos = [f for f in os.listdir(pasta_comentarios) if f.endswith(".txt")]
    caminho_arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(os.path.join(pasta_comentarios, f)))

    # Lendo o arquivo de texto mais recente
    caminho_arquivo = os.path.join(pasta_comentarios, caminho_arquivo_mais_recente)
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    # Processando os comentários e realizando a análise de sentimentos
    resultados = []
    for linha in linhas:
        try:
            usuario, comentario = linha.split(":", 1)  # Separando o nome do comentário
            sentimento = analisar_sentimento(comentario.strip())  # Analisando o sentimento do comentário
            resultados.append({"usuario": usuario.strip(), "comentario": comentario.strip(), "sentimento": sentimento})
        except ValueError:
            continue  # Caso a linha não tenha o formato esperado (usuário: comentário)

    return resultados
