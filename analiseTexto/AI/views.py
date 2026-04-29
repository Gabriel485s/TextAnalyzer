from django.shortcuts import render
from django.http import HttpRequest
import string
import nltk
from pathlib import Path
import pickle
import json

nltk.download('punkt')
nltk.download('stopwords')

# Create your views here.

stop_words = set(nltk.corpus.stopwords.words('portuguese'))

def extrair_caracteristicas(palavras):
    return {palavra: True for palavra in palavras}

def preparar_texto(texto):
    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    palavras = nltk.tokenize.word_tokenize(texto, language='portuguese')

    palavras_filtradas = []
    for palavra in palavras:
        if palavra not in stop_words and len(palavra) > 2:
            palavras_filtradas.append(palavra)

    return palavras_filtradas

pasta_atual = Path(__file__).parent
caminho_modelo = pasta_atual / "LogisticRegression.pickle"
caminho_metricas = pasta_atual / "metricas_modelo.json"

with open(caminho_modelo, "rb") as arquivo:
    classificador = pickle.load(arquivo)
    
with open(caminho_metricas, "rb") as arquivo_metricas:
    metricas = json.load(arquivo_metricas)

def index(request: HttpRequest):
    contexto = {
        "mostrar_grafico": False,
        "positivos": 0,
        "negativos": 0,
        "neutros": 0
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

            print("resultado:", resultado)
            print("qtd palavras:", len(palavras))
            print("positivo:", probabilidades.prob("positivo"))
            print("negativo:", probabilidades.prob("negativo"))
            print("neutro:", probabilidades.prob("neutro"))

            mostrar_grafico = True

            contexto = {
                "mostrar_grafico": mostrar_grafico,
                "positivos": positivos,
                "negativos": negativos,
                "neutros": neutros,
                "texto": texto,
                "resultado": resultado,
                "acuracia": metricas["acuracia"],
                "precisao": metricas["precisao"],
                "tempo_treino": round(metricas["tempo_treinamento_ms"] / 1000, 4),
                "tempo_previsao": round(metricas["tempo_previsao_ms"] / 1000, 4),
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

def analise_5_dias(request: HttpRequest):
    contexto = {
        "mostrar_grafico": True,
        "positivos": 30,
        "negativos": 30,
        "neutros": 40
    }
    return render(request, 'result.html', contexto)