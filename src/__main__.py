from fastapi import FastAPI
import sys
from pathlib import Path
import uvicorn
import os
import json
import logging
import re
import threading
import queue
from datetime import datetime

# Ajouter le dossier 'src' à sys.path
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent / "service" / "controller"))
sys.path.append(str(Path(__file__).resolve().parent / "llm"))

# Importer les modules
from service.controller.HandlingRequest import handling_request
from service.chromadb.ChromaFunctions import search_in_collection_text

# Définir le chemin vers le modèle
modelPath = "./Meta-Llama-3.1-8B-Instruct"

# Créer l'application FastAPI
app = FastAPI()

@app.get("/")
def index():
    """
    Endpoint racine : retourne un message de bienvenue.
    """
    return {"data": "Bonjour, bienvenu sur RAGAdmin !"}

@app.post("/{req}")
def requete(req: str):
    context = search_in_collection_text("codedelaroute", req, 1)
    """
    Endpoint POST pour traiter une requête donnée.

    Arguments:
    - req : la requête (question) à envoyer au modèle.

    Retourne:
    - La réponse générée par le modèle.
    """
    try:
        response = handling_request(req, modelPath, context)
        return {"data": response}
    except Exception as e:
        return {"error": f"Une erreur est survenue : {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
