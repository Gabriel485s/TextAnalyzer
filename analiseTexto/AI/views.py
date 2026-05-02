from django.shortcuts import render, redirect
from django.http import HttpRequest
import string
import nltk
from pathlib import Path
import pickle
import json
from .gemini_analysis import gerar_resposta

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
    resposta = ""
    
    contexto = {
        "mostrar_grafico": mostrar_grafico,
        "positivos": positivos,
        "negativos": negativos,
        "neutros": neutros,
        "texto": texto,
        "resultado": resultado,
        "resposta": resposta
    }
    
    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()

        if texto:
            palavras = preparar_texto(texto)
            
            texto_formatado = ' '.join(palavras)
            
            try:
                resposta = gerar_resposta(texto_formatado)
                
                if resposta is None:
                    
                    caracteristicas = extrair_caracteristicas(palavras)

                    resultado = classificador.classify(caracteristicas)
                    probabilidades = classificador.prob_classify(caracteristicas)

                    positivos = round(probabilidades.prob("positivo") * 100, 2)
                    negativos = round(probabilidades.prob("negativo") * 100, 2)
                    neutros = round(probabilidades.prob("neutro") * 100, 2)

                    mostrar_grafico = True
                            
                    contexto = {
                        "mostrar_grafico": mostrar_grafico,
                        "positivos": positivos,
                        "negativos": negativos,
                        "neutros": neutros,
                        "texto": texto,
                        "resultado": resultado,
                        "resposta": resposta,
                        "acuracia": metricas["acuracia"],
                        "precisao": metricas["precisao"],
                        "tempo_treino": round(metricas["tempo_treinamento_ms"] / 1000, 4),
                        "tempo_previsao": round(metricas["tempo_previsao_ms"] / 1000, 4),
                    }
                    
                    request.session["analise_inserida"] = contexto
                    request.session.modified = True

                    return redirect("/analise/?tipo=inserida")
                    
        
                else:
                    
                    resposta_limpa = resposta.strip().lower().replace(".", "")

                    if resposta_limpa in ["inválido", "invalid", "invalido"]:
                        return redirect("/")
                    
                    caracteristicas = extrair_caracteristicas(palavras)

                    resultado = classificador.classify(caracteristicas)
                    probabilidades = classificador.prob_classify(caracteristicas)

                    positivos = round(probabilidades.prob("positivo") * 100, 2)
                    negativos = round(probabilidades.prob("negativo") * 100, 2)
                    neutros = round(probabilidades.prob("neutro") * 100, 2)

                    mostrar_grafico = True
                            
                    contexto = {
                        "mostrar_grafico": mostrar_grafico,
                        "positivos": positivos,
                        "negativos": negativos,
                        "neutros": neutros,
                        "texto": texto,
                        "resultado": resultado,
                        "resposta": resposta,
                        "acuracia": metricas["acuracia"],
                        "precisao": metricas["precisao"],
                        "tempo_treino": round(metricas["tempo_treinamento_ms"] / 1000, 4),
                        "tempo_previsao": round(metricas["tempo_previsao_ms"] / 1000, 4),
                    }
                    
                    request.session["analise_inserida"] = contexto
                    request.session.modified = True

                    return redirect("/analise/?tipo=inserida")
                    
            except Exception as erro:
                
                print(f"Ocorreu o erro: {erro}")
                
                return redirect("/")
                
        
    elif request.method == 'GET':
        
        if request.GET.get("tipo") == "5_dias":
            mostrar_grafico = True
            
            contexto = {
            "mostrar_grafico": mostrar_grafico,
            "positivos": 30,
            "negativos": 30,
            "neutros": 40,
            }
        
        
            return render(request, "result.html", contexto)
        
        elif request.GET.get("tipo") == "inserida":
            
            contexto = request.session.get("analise_inserida")

            if contexto is None:
                return render(request, "index.html", {
                    "erro": "Nenhuma análise de notícia inserida foi encontrada."
                })

            return render(request, "result.html", contexto)

    return render(request, 'index.html', contexto)
