import chromadb
from chromadb.utils import embedding_functions
import hashlib
import os
from typing import List, Any, Optional
from .base_repository import DocumentRepository

class ChromaRepository(DocumentRepository):
    """Implémentation ChromaDB du repository de documents"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8001):
        self.host = host
        self.port = port
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='sentence-transformers/all-mpnet-base-v2'
        )
        self.client = self._get_client()

    def _get_client(self):
        """Obtient une instance du client ChromaDB"""
        try:
            return chromadb.HttpClient(host=self.host, port=self.port)
        except Exception as e:
            raise ConnectionError(f"Impossible de se connecter à ChromaDB: {str(e)}")

    def _generate_file_hash(self, file_path: str) -> str:
        """Génère un hash stable pour un fichier"""
        hasher = hashlib.md5()
        abs_path = os.path.abspath(file_path)
        hasher.update(abs_path.encode('utf-8'))
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def create_collection(self, collection_name: str) -> Any:
        """Crée ou récupère une collection"""
        try:
            collection = self.client.get_collection(
                collection_name,
                embedding_function=self.embedding_function
            )
            return collection
        except Exception:
            collection = self.client.create_collection(
                collection_name,
                embedding_function=self.embedding_function
            )
            return collection

    def delete_collection(self, collection_name: str) -> None:
        """Supprime une collection"""
        try:
            self.client.delete_collection(collection_name)
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de la collection: {str(e)}")

    def search_by_text(self, collection_name: str, query_text: str, k: int = 1) -> List[dict]:
        """Recherche des documents par texte"""
        collection = self.create_collection(collection_name)
        try:
            results = collection.query(
                query_texts=[query_text],
                n_results=k
            )
            return results
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche: {str(e)}")

    def search_by_embedding(self, collection_name: str, query_embedding: List[float], k: int = 1) -> List[dict]:
        """Recherche des documents par embedding"""
        collection = self.create_collection(collection_name)
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            return results
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche: {str(e)}")

    def add_document(self, file_path: str, collection_name: str) -> None:
        """Ajoute un document à la collection"""
        collection = self.create_collection(collection_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Création d'un ID unique basé sur le hash du fichier
            doc_id = self._generate_file_hash(file_path)
            
            collection.add(
                documents=[content],
                metadatas=[{"source": file_path}],
                ids=[doc_id]
            )
        except Exception as e:
            raise ValueError(f"Erreur lors de l'ajout du document: {str(e)}")

    def delete_document(self, file_path: str, collection_name: str) -> None:
        """Supprime un document de la collection"""
        collection = self.create_collection(collection_name)
        try:
            # Recherche des documents contenant le chemin du fichier
            results = collection.get(
                where={"source": file_path}
            )
            if results and results['ids']:
                collection.delete(ids=results['ids'])
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression du document: {str(e)}")

    def get_collection_contents(self, collection_name: str) -> List[dict]:
        """Récupère le contenu d'une collection"""
        collection = self.create_collection(collection_name)
        try:
            return collection.get()
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération du contenu: {str(e)}")
