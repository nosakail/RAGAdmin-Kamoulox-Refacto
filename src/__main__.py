from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Ajouter le dossier 'src' à sys.path
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent / "service" / "controller"))
sys.path.append(str(Path(__file__).resolve().parent / "llm"))

# Importer les modules
from service.controller.handling_request import handling_request
from service.chromadb.chromafunctions import search_in_collection_text

# Définir le chemin vers le modèle
modelPath = "./Meta-Llama-3.1-8B-Instruct"

# Créer l'application FastAPI
app = FastAPI()

# 1. Ajouter une authentification par API key
API_KEY_NAME = "X-API-Key"
API_KEY = "your-secure-api-key"  # À stocker de manière sécurisée (variables d'environnement)
api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key

# 2. Configurer CORS de manière restrictive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-domaine.com"],  # Liste des domaines autorisés
    allow_credentials=False,  # Désactive les cookies cross-origin
    allow_methods=["GET", "POST"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # Headers autorisés
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def index():
    """
    Endpoint racine : retourne un message de bienvenue.
    """
    return {"data": "Bonjour, bienvenu sur RAGAdmin !"}

@app.post("/{req}")
@limiter.limit("5/minute")  # Limite à 5 requêtes par minute par IP
async def requete(
    req: str,
    api_key: str = Depends(verify_api_key)  # Protection par API key
):
    """
    Endpoint POST pour traiter une requête donnée.

    Arguments:
    - req : la requête (question) à envoyer au modèle.

    Retourne:
    - La réponse générée par le modèle.
    """
    try:
        context = search_in_collection_text("codedelaroute", req, 1)
        response = handling_request(req, modelPath, context)
        return {"data": response}
    except Exception as e:
        return {"error": f"Une erreur est survenue : {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
