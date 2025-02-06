from abc import ABC, abstractmethod
from typing import List, Any, Optional

class DocumentRepository(ABC):
    """Interface abstraite pour le repository de documents"""
    
    @abstractmethod
    def create_collection(self, collection_name: str) -> Any:
        """Crée une nouvelle collection"""
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        """Supprime une collection existante"""
        pass
    
    @abstractmethod
    def search_by_text(self, collection_name: str, query_text: str, k: int = 1) -> List[dict]:
        """Recherche des documents par texte"""
        pass
    
    @abstractmethod
    def search_by_embedding(self, collection_name: str, query_embedding: List[float], k: int = 1) -> List[dict]:
        """Recherche des documents par embedding"""
        pass
    
    @abstractmethod
    def add_document(self, file_path: str, collection_name: str) -> None:
        """Ajoute un document à la collection"""
        pass
    
    @abstractmethod
    def delete_document(self, file_path: str, collection_name: str) -> None:
        """Supprime un document de la collection"""
        pass
    
    @abstractmethod
    def get_collection_contents(self, collection_name: str) -> List[dict]:
        """Récupère le contenu d'une collection"""
        pass
