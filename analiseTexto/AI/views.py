from django.shortcuts import render
from .forms import IaForm
from django.http import HttpRequest
import string
import nltk
nltk.download('punkt_tab')



# Create your views here.

def index(request:HttpRequest):
    
    formulario = IaForm()

    contexto = {
        "form": formulario
    }

    return render(request, 'index.html', contexto)



def analise(request: HttpRequest):
    mostrar_grafico = False
    positivos = 0
    negativos = 0

    if request.method == 'POST':
        formulario = IaForm(request.POST)

        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            minusculo = texto.lower()

            texto_limpo = minusculo.translate(str.maketrans('', '', string.punctuation))

            stop_words = nltk.corpus.stopwords.words('portuguese')
            palavras = nltk.tokenize.word_tokenize(texto_limpo, language='portuguese')

            frase_filtrada = []

            for frase in palavras:
                if frase not in stop_words:
                    frase_filtrada.append(frase)

            print(frase_filtrada)

            positivos = 10 #valor exemplo
            negativos = 5 #valor exemplo
            mostrar_grafico = True

    else:
        formulario = IaForm()

    contexto = {
        "form": formulario,
        "mostrar_grafico": mostrar_grafico,
        "positivos": positivos,
        "negativos": negativos
    }

    return render(request, 'index.html', contexto)