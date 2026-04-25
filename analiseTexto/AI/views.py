from django.shortcuts import render
from django.http import HttpRequest
import string
import nltk
from pathlib import Path
import pickle

nltk.download('punkt_tab')

# Create your views here.

def extrair_caracteristicas(palavras):
    return {palavra: True for palavra in palavras}

def preparar_texto(texto):
    
    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))

    palavras = nltk.tokenize.word_tokenize(texto, language='portuguese')

    palavras_filtradas = []

    for palavra in palavras:
        palavras_filtradas.append(palavra)

    return palavras_filtradas

pasta_atual = Path(__file__).parent
caminho_modelo = pasta_atual / "NaiveBayes.pickle"

with open(caminho_modelo, "rb") as arquivo:
    classificador = pickle.load(arquivo)


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
    neutros = 0
    texto = ""
    resultado = ""

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()

        if texto:

            palavras = preparar_texto(texto)

            caracteristicas = extrair_caracteristicas(palavras)

            resultado = classificador.classify(caracteristicas)

            probabilidades = classificador.prob_classify(caracteristicas)

            positivos = round(probabilidades.prob("positivo") * 100, 2)
            negativos = round(probabilidades.prob("negativo") * 100, 2)
            neutros = round(probabilidades.prob("neutro") * 100, 2)

            print(positivos + negativos + neutros)
            
            mostrar_grafico = True

            contexto = {
                "mostrar_grafico": mostrar_grafico,
                "positivos": positivos,
                "negativos": negativos,
                "neutros": neutros,
                "texto": texto,
                "resultado": resultado,
            }

            return render(request, "result.html", contexto)

    contexto = {
        "mostrar_grafico": mostrar_grafico,
        "positivos": positivos,
        "negativos": negativos,
        "neutros": neutros,
        "texto": texto,
        "resultado": resultado,
    }
    
    return render(request, 'index.html', contexto)