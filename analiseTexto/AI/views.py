from django.shortcuts import render
from django.http import HttpRequest
import string
import nltk
nltk.download('punkt_tab')



# Create your views here.

def index(request:HttpRequest):
    
    contexto = {
        "mostrar_grafico": False,
        "positivos": 0,
        "negativos": 0
    }

    return render(request, 'index.html', contexto)



def analise(request: HttpRequest):
    mostrar_grafico = False
    positivos = 0
    negativos = 0
    texto = ""

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        
        if texto:
            minusculo = texto.lower()

            texto_limpo = minusculo.translate(str.maketrans('', '', string.punctuation))

            stop_words = nltk.corpus.stopwords.words('portuguese')
            palavras = nltk.tokenize.word_tokenize(texto_limpo, language='portuguese')

            frase_filtrada = []

            for frase in palavras:
                if frase not in stop_words:
                    frase_filtrada.append(frase)

            print(frase_filtrada)

            positivos = 10
            negativos = 5
            mostrar_grafico = True

    contexto = {
        "mostrar_grafico": mostrar_grafico,
        "positivos": positivos,
        "negativos": negativos,
        "texto": texto
    }

    return render(request, 'index.html', contexto)