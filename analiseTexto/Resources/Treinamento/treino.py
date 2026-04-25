import nltk
import json
import string
from pathlib import Path
#from nltk.classify.scikitlearn import SklearnClassifier
import random
import pickle

#from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
#from sklearn.linear_model import LogisticRegression, SGDClassifier
#from sklearn.svm import SVC, LinearSVC, NuSVC

def extrair_caracteristicas(palavras):
    return {palavra: True for palavra in palavras}
try:

    pasta_atual = Path(__file__).parent
    caminho = pasta_atual / "classified_articles_rotulado.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados_processados = []
    
    for noticia in dados:
        conteudo = noticia["content"]
        categoria = noticia["training_label"]

        conteudo = conteudo.lower()
        conteudo = conteudo.translate(str.maketrans('', '', string.punctuation))

        palavras = nltk.tokenize.word_tokenize(conteudo, language='portuguese')

        palavras_filtradas = []

        for palavra in palavras:
            palavras_filtradas.append(palavra)
        
        caracteristicas = extrair_caracteristicas(palavras_filtradas)

        dados_processados.append((caracteristicas, categoria))
        
    random.shuffle(dados_processados)

    tamanho_treino = int(len(dados_processados) * 0.8)

    dados_treinamento = dados_processados[:tamanho_treino]
    dados_teste = dados_processados[tamanho_treino:]

    #classificador = nltk.NaiveBayesClassifier.train(dados_treinamento)
    
    classificador_f = open("NaiveBayes.pickle", "rb")
    
    classificador = pickle.load(classificador_f)
    
    classificador_f.close()

    acuracia = nltk.classify.accuracy(classificador, dados_teste)

    print(f"Naive Bayes Acurácia Original: {acuracia:.2%}")

    classificador.show_most_informative_features(15)
    
    #MultinomialNB - 7º lugar
    
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
    
    #LogisticRegression 2º lugar - Outliers Atrapalham
    
    #LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    #LogisticRegression_classifier.train(dados_treinamento)
    #acuraciaLR = nltk.classify.accuracy(LogisticRegression_classifier, dados_teste)
    #print(f"LogisticRegression_classifier Acurácia: {acuraciaLR:.2%}")
    
    #SGDClassifier 5º lugar
    
    #SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    #SGDClassifier_classifier.train(dados_treinamento)
    #acuraciaSGD = nltk.classify.accuracy(SGDClassifier_classifier, dados_teste)
    #print(f"SGDClassifier_classifier Acurácia: {acuraciaSGD:.2%}")
    
    #SVC_classifier 6º lugar
    
    #SVC_classifier = SklearnClassifier(SVC())
    #SVC_classifier.train(dados_treinamento)
    #acuraciaSVC = nltk.classify.accuracy(SVC_classifier, dados_teste)
    #print(f"SVC_classifier Acurácia: {acuraciaSVC:.2%}")
    
    #LinearSVC 4º lugar
    
    #LinearSVC_classifier = SklearnClassifier(LinearSVC())
    #LinearSVC_classifier.train(dados_treinamento)
    #acuraciaLSVC = nltk.classify.accuracy(LinearSVC_classifier, dados_teste)
    #print(f"LinearSVC_classifier Acurácia: {acuraciaLSVC:.2%}")
    
    #NuSVC 3º lugar
    
    #NuSVC_classifier = SklearnClassifier(NuSVC(nu=0.3))
    #NuSVC_classifier.train(dados_treinamento)
    #acuraciaNUSVC = nltk.classify.accuracy(NuSVC_classifier, dados_teste)
    #print(f"NuSVC_classifier Acurácia: {acuraciaNUSVC:.2%}")
    
except Exception as e:
    print(f"Ocorreu um erro: {e}")

