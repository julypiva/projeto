# 🚀 Pipeline de Logs com IA para análise de comentários nocivos

**Resumo:** 
Este projeto automatiza a coleta e análise de sentimentos de comentários públicos do Instagram, classificando-os em positivo, negativo ou neutro. A solução utiliza técnicas de tradução, análise de sentimentos com VADER e dicionários personalizados para aprimorar a precisão, apresentando os resultados em uma interface web intuitiva.

---

## 🎯 Objetivo
O objetivo do projeto é desenvolver um sistema que permita a análise automática da percepção pública em redes sociais por meio da classificação de sentimentos em comentários do Instagram. A motivação é facilitar a avaliação de marcas ou perfis digitais, utilizando conceitos de linguagens formais e autômatos para estruturar a classificação e refinamento dos dados textuais coletados.

---

## 👨‍💻 Tecnologias Utilizadas
- Python: Selenium, Pandas, Pyautogui, Pyperclip, Os
- GoogleTranslator
- vaderSentiment

---

## 🗂️ Estrutura do Projeto
```
📦 Projeto
├── 📁 Pastas
│   ├── __pycache/
│   ├── log comentários/comentarios_DD_MM_YYYY_HH_MM.txt
│   ├── log_analise/analise_sentimento_DD_MM_YYYY_HH_MM.txt
│   |── templates/estatistica.html|index.html|sobre.html
│   └── static/hateShield_logo.png|style.css
├── app.py
├── analise_sentimento.py
├── selenium_script.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Como Executar

### ✅ Rodando Localmente

1. Clone o repositório:

```
git clone https://github.com/julypiva/projeto
cd projeto
```

2. Crie o ambiente virtual e ative:

```
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Execute a aplicação:

```
python main.py
```

---

## 📸 Demonstrações

- **Tela inicial:**
![image](https://github.com/user-attachments/assets/474113d4-c842-485c-b3b3-72c79608473e)

- **Exemplo de funcionalidade:**
![image](https://github.com/user-attachments/assets/501b508f-1c43-4d3a-9bb8-ec92941cbb0d)

- **Resultados esperados:**
![image](https://github.com/user-attachments/assets/84cf208b-e4db-4cb1-a35d-66228124b778)

---

## 👥 Equipe

| Nome | GitHub |
|------|--------|
| Julya da Mota Piva | [@julypiva](https://github.com/julypiva) |
| Isabelly Constantino Pagels | [@isapagels](https://github.com/isapagels) |

---

## 🧠 Disciplina Envolvida

- Linguagens Formais e Autômatos

---

## 🏫 Informações Acadêmicas

- Universidade: **Universidade Braz Cubas**
- Curso: **Ciência da Computação**
- Semestre: 7º
- Período: Noite
- Professora orientadora: **Dra. Andréa Ono Sakai**
- Evento: **Mostra de Tecnologia 1º Semestre de 2025**
- Local: Laboratório 12
- Data: 06 de junho de 2025

---

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
