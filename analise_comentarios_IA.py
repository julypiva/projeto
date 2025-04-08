from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import os

# Baixar os dados necessários do VADER
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

# Definir o caminho da pasta onde os arquivos de comentários são salvos
pasta_comentarios = r"C:\Users\julya.piva\Desktop\projeto\log_comentarios"

# Encontrar o arquivo mais recente na pasta de comentários
arquivos = [f for f in os.listdir(pasta_comentarios) if f.endswith(".txt")]
caminho_arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(os.path.join(pasta_comentarios, f)))

# Lendo o arquivo de texto mais recente
caminho_arquivo = os.path.join(pasta_comentarios, caminho_arquivo_mais_recente)
with open(caminho_arquivo, "r", encoding="utf-8") as file:
    linhas = file.readlines()

# Criando nome do arquivo de saída com data e hora
agora = datetime.now().strftime("%d_%m_%Y_%H_%M")
nome_arquivo = f"C:\\Users\\julya.piva\\Desktop\\projeto\\log_analise\\analise_sentimento_{agora}.txt"

# Escrevendo os resultados no novo arquivo
total_resultados = []
for linha in linhas:
    usuario, comentario = linha.split(":", 1)  # Separando o nome do comentário
    sentimento = analisar_sentimento(comentario.strip())  # Analisando o sentimento do comentário
    resultado = f"Comentário: {comentario.strip()}\nSentimento: {sentimento}\n"
    total_resultados.append(resultado)

# Salvando os resultados no arquivo
with open(nome_arquivo, "w", encoding="utf-8") as output_file:
    output_file.writelines("\n".join(total_resultados))

print(f"Resultados salvos em {nome_arquivo}")
