from typing import Optional, List, Dict, Any
from repositories.repository_factory import RepositoryFactory
from repositories.base_repository import DocumentRepository

class DocumentService:
    """Service pour gérer les opérations sur les documents"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8001):
        self.repository: DocumentRepository = RepositoryFactory.create_repository(
            repo_type="chroma",
            host=host,
            port=port
        )
    
    def import_document(self, file_path: str, collection_name: str) -> None:
        """
        Importe un document dans une collection
        
        Args:
            file_path: Chemin vers le fichier à importer
            collection_name: Nom de la collection
        """
        try:
            self.repository.add_document(file_path, collection_name)
            print(f"Document {file_path} importé avec succès dans la collection {collection_name}")
        except Exception as e:
            print(f"Erreur lors de l'import du document: {str(e)}")
    
    def search_documents(self, collection_name: str, query: str, k: int = 1) -> Optional[List[Dict[str, Any]]]:
        """
        Recherche des documents dans une collection
        
        Args:
            collection_name: Nom de la collection
            query: Texte de recherche
            k: Nombre de résultats à retourner
            
        Returns:
            Liste des résultats ou None si erreur
        """
        try:
            results = self.repository.search_by_text(collection_name, query, k)
            return results
        except Exception as e:
            print(f"Erreur lors de la recherche: {str(e)}")
            return None
    
    def delete_collection(self, collection_name: str) -> None:
        """
        Supprime une collection
        
        Args:
            collection_name: Nom de la collection à supprimer
        """
        try:
            self.repository.delete_collection(collection_name)
            print(f"Collection {collection_name} supprimée avec succès")
        except Exception as e:
            print(f"Erreur lors de la suppression de la collection: {str(e)}")
    
    def create_collection(self, collection_name: str) -> None:
        """
        Crée une nouvelle collection
        
        Args:
            collection_name: Nom de la collection à créer
        """
        try:
            self.repository.create_collection(collection_name)
            print(f"Collection {collection_name} créée avec succès")
        except Exception as e:
            print(f"Erreur lors de la création de la collection: {str(e)}")
    
    def get_collection_contents(self, collection_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Récupère le contenu d'une collection
        
        Args:
            collection_name: Nom de la collection
            
        Returns:
            Contenu de la collection ou None si erreur
        """
        try:
            return self.repository.get_collection_contents(collection_name)
        except Exception as e:
            print(f"Erreur lors de la récupération du contenu: {str(e)}")
            return None
