import json
import requests
from bs4 import BeautifulSoup
import nltk
import string

all_words = []

resultado = []

try:

    with open(r"C:\Users\User\OneDrive\Documentos\VS-CodeProjects\APS\analiseTexto\Resources\Web_Scrapping\extracted_urls.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    #for item in dados:
        #pagina = requests.get(item["url"])

        #dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

        #frases = dados_pagina.find_all('div', class_="mc-column content-text active-extra-styles")

        #for div in frases:

            #texto = div.get_text(" ", strip=True)
            
            
            #texto = texto.lower().translate(str.maketrans('', '', string.punctuation))
            #palavras = texto.split()
            #all_words.extend(palavras)
               
    for item in dados:
        
        pagina = requests.get(item["url"])

        dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

        frases = dados_pagina.find_all('div', class_="mc-column content-text active-extra-styles")

        textos = []

        for div in frases:
            texto = div.get_text(" ", strip=True)
            if texto:
                textos.append(texto)

        texto_final = " ".join(textos)

        resultado.append({
            "url": item["url"],
            "texto": texto_final
        })

    with open(r"C:\Users\User\OneDrive\Documentos\VS-CodeProjects\APS\analiseTexto\Resources\Web_Scrapping\textos_extraidos.json", "w", encoding="utf-8") as arquivo_saida:
        json.dump(resultado, arquivo_saida, ensure_ascii=False, indent=4)

    print("JSON salvo com sucesso.")
 

except Exception as e:
    print(f"Ocorreu um erro: {e}")

