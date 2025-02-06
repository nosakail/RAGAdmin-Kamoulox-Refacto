from typing import Optional
from .base_repository import DocumentRepository
from .chroma_repository import ChromaRepository

class RepositoryFactory:
    """Factory pour créer des instances de repositories"""
    
    @staticmethod
    def create_repository(
        repo_type: str = "chroma",
        host: str = "127.0.0.1",
        port: int = 8001
    ) -> DocumentRepository:
        """
        Crée une instance de repository selon le type spécifié
        
        Args:
            repo_type: Type de repository ("chroma" pour l'instant)
            host: Hôte du service de base de données
            port: Port du service de base de données
            
        Returns:
            Une instance de DocumentRepository
            
        Raises:
            ValueError: Si le type de repository n'est pas supporté
        """
        if repo_type.lower() == "chroma":
            return ChromaRepository(host=host, port=port)
        else:
            raise ValueError(f"Type de repository non supporté: {repo_type}")
