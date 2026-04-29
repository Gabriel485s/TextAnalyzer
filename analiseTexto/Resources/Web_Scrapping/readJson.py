import json
import requests
from bs4 import BeautifulSoup
import nltk
import string

all_words = []

try:
    #for item in dados:
        #pagina = requests.get(item["url"])

        #dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

        #frases = dados_pagina.find_all('div', class_="mc-column content-text active-extra-styles")

        #for div in frases:

            #texto = div.get_text(" ", strip=True)
            
            
            #texto = texto.lower().translate(str.maketrans('', '', string.punctuation))
            #palavras = texto.split()
            #all_words.extend(palavras)
               
    pagina = requests.get("https://boanoticiabrasil.com.br/sustentabilidade/brasil-reduz-desmatamento-queda-global-2025/")

    dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

    frases = dados_pagina.find_all("p")

    textos = []

    for tag in frases:
        texto = tag.get_text(" ", strip=True)
        if texto:
            textos.append(texto)

    texto_final = " ".join(textos)

    print(texto_final)
 

except Exception as e:
    print(f"Ocorreu um erro: {e}")

