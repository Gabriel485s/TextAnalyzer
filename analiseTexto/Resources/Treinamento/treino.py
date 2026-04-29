import nltk
import json
import string
from pathlib import Path
import random
import pickle
from time import time

from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import precision_score

nltk.download('punkt')
nltk.download('stopwords')

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

def formatar_tempo(inicio, fim):
    
    return (fim - inicio) * 1000

try:
    pasta_atual = Path(__file__).parent
    caminho = pasta_atual / "dataset_noticias.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados_processados = []

    for noticia in dados:
        conteudo = noticia["texto"]
        categoria = noticia["sentimento"]

        palavras_filtradas = preparar_texto(conteudo)
        caracteristicas = extrair_caracteristicas(palavras_filtradas)

        dados_processados.append((caracteristicas, categoria))

    random.shuffle(dados_processados)

    tamanho_treino = int(len(dados_processados) * 0.8)
    dados_treinamento = dados_processados[:tamanho_treino]
    dados_teste = dados_processados[tamanho_treino:]

    # classificador = nltk.NaiveBayesClassifier.train(dados_treinamento)

    # acuracia = nltk.classify.accuracy(classificador, dados_teste)
    # print(f"Naive Bayes Acurácia: {acuracia:.2%}")
    
    LogisticRegression_classificador = SklearnClassifier(LogisticRegression())
    
    inicio = time()
    
    LogisticRegression_classificador.train(dados_treinamento)
    
    fim = time()
    
    tempo_treinamento = formatar_tempo(inicio, fim)
    
    acuraciaLR = nltk.classify.accuracy(LogisticRegression_classificador, dados_teste)
    
    y_true = []
    y_pred = []
    
    inicio_previsao = time()
    
    for features, classe_real in dados_teste:
        classe_prevista = LogisticRegression_classificador.classify(features)
        y_true.append(classe_real)
        y_pred.append(classe_prevista)

    fim_previsao = time()
    
    tempo_previsao = formatar_tempo(inicio_previsao, fim_previsao)
    
    precisao = precision_score(y_true, y_pred, average='macro', zero_division=0)
    
    print(f"LogisticRegression_classificador Acurácia: {acuraciaLR:.2%}")

    metricas = {
        "acuracia": round(acuraciaLR * 100, 2),
        "precisao": round(precisao * 100, 2),
        "tempo_treinamento_ms": round(tempo_treinamento, 2),
        "tempo_previsao_ms": round(tempo_previsao / len(dados_teste), 2)
    }
    
    with open(pasta_atual / "metricas_modelo.json", "w", encoding="utf-8") as f:
        json.dump(metricas, f, ensure_ascii=False, indent=4)
    
    with open(pasta_atual / "LogisticRegression.pickle", "wb") as f:
        pickle.dump(LogisticRegression_classificador, f)
    
     #MultinomialNB - 6º lugar
    
    #MNB_classifier = SklearnClassifier(MultinomialNB())
    #MNB_classifier.train(dados_treinamento)
    #acuraciaMNB = nltk.classify.accuracy(MNB_classifier, dados_teste)
    #print(f"MNB_classifier Acurácia: {acuraciaMNB:.2%}")

    #GaussianNB - Deu erro
    
    #GaussianNB_classifier = SklearnClassifier(GaussianNB())
    #GaussianNB_classifier.train(dados_treinamento)
    #acuraciaGNB = nltk.classify.accuracy(GaussianNB_classifier, dados_teste)
    #print(f"GaussianNB_classifier Acurácia: {acuraciaGNB:.2%}")
    
    #BernoulliNB 8º lugar
    
    #BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    #BernoulliNB_classifier.train(dados_treinamento)
    #acuraciaBNB = nltk.classify.accuracy(BernoulliNB_classifier, dados_teste)
    #print(f"BernoulliNB_classifier Acurácia: {acuraciaBNB:.2%}")
    
    #LogisticRegression 1º lugar - Outliers Atrapalham
    
    #LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    #LogisticRegression_classifier.train(dados_treinamento)
    #acuraciaLR = nltk.classify.accuracy(LogisticRegression_classifier, dados_teste)
    #print(f"LogisticRegression_classifier Acurácia: {acuraciaLR:.2%}")
    
    #SGDClassifier 2º lugar
    
    #SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    #SGDClassifier_classifier.train(dados_treinamento)
    #acuraciaSGD = nltk.classify.accuracy(SGDClassifier_classifier, dados_teste)
    #print(f"SGDClassifier_classifier Acurácia: {acuraciaSGD:.2%}")
    
    #SVC_classifier 5º lugar
    
    #SVC_classifier = SklearnClassifier(SVC())
    #SVC_classifier.train(dados_treinamento)
    #acuraciaSVC = nltk.classify.accuracy(SVC_classifier, dados_teste)
    #print(f"SVC_classifier Acurácia: {acuraciaSVC:.2%}")
    
    #LinearSVC 3º lugar
    
    #LinearSVC_classifier = SklearnClassifier(LinearSVC())
    #LinearSVC_classifier.train(dados_treinamento)
    #acuraciaLSVC = nltk.classify.accuracy(LinearSVC_classifier, dados_teste)
    #print(f"LinearSVC_classifier Acurácia: {acuraciaLSVC:.2%}")
    
    #NuSVC 4º lugar
    
    #NuSVC_classifier = SklearnClassifier(NuSVC(nu=0.3))
    #NuSVC_classifier.train(dados_treinamento)
    #acuraciaNUSVC = nltk.classify.accuracy(NuSVC_classifier, dados_teste)
    #print(f"NuSVC_classifier Acurácia: {acuraciaNUSVC:.2%}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")