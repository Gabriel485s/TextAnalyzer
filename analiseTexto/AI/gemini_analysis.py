from google import genai
import json
from pathlib import Path
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv
import os
import time

load_dotenv()

models = ["gemini-3-flash-preview", "gemini-2.5-flash"]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client()

instructions = """you are an environmental analyst with extensive expertise in categorizing and interpreting environmental texts. I request your advanced skills to analyze the provided text concerning environmental issues and accurately classify its content into specific, well-defined topics.
    Please ensure your analysis includes:
    Identification of primary themes such as Fires, Floods, Wildlife, Pollution, Climate Change, Conservation Efforts, or other relevant categories.
    Leverage your specialized knowledge and analytical experience to deliver a comprehensive classification that facilitates clear understanding and targeted responses to the environmental issues presented.
    you should only state the rating, nothing else
    return only one result, do not use a comma citing several others,
    do not differentiate the topics with things like "Extreme" or any other adjectives, just state the topic,
    only in Brazilian Portuguese and if it is not an environmental issue you must always say "Invalid"
    
    """

def gerar_resposta(prompt, tentativas=3):
    
    for model in models:
        for tentativa in range(1, tentativas + 1):
            
            try:
                if (model == "gemini-2.5-flash"):
                    
                    resposta = client.models.generate_content(
                        model=model,
                        config=types.GenerateContentConfig(
                            system_instruction=instructions,
                        ),
                        contents=prompt,
                    )
                else:
                    resposta = client.models.generate_content(
                        model=model,
                        config=types.GenerateContentConfig(
                            system_instruction=instructions,
                            thinking_config=types.ThinkingConfig(thinking_level="low"),
                        ),
                        contents=prompt,
                    )

                return resposta.text

            except ClientError as erro:
                erro_texto = str(erro).lower()
                
                if "429" in erro_texto or "resource_exhausted" in erro_texto or "quota" in erro_texto:
                    print("Limite diário ou cota da API atingida.")
                    break

                if "503" in erro_texto and tentativa < tentativas:
                    print("Erro 503. Tentando novamente...")
                    time.sleep(2)
                    
                    continue

                print(f"Erro no modelo {model}: {erro}")
                break

            except Exception as erro:
                erro_texto = str(erro).lower()

                if "429" in erro_texto or "resource_exhausted" in erro_texto or "quota" in erro_texto:
                    print("Limite diário ou cota da API atingida.")
                    break

                if "503" in erro_texto and tentativa < tentativas:
                    print("Erro 503. Tentando novamente...")
                    time.sleep(2)
                    
                    continue

                print(f"Erro inesperado no modelo {model}: {erro}")
                break
        
    print("Nenhum modelo conseguiu gerar resposta.")
    return None
