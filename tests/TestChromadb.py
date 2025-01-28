import pytest
from pathlib import Path
import chromadb.errors

# Imports spécifiques des fonctions ChromaDB
from src.service.chromadb.ChromaFunctions import (
    get_client,
    create_collection,
    search_in_collection_text,
    delete_collection
)

class TestChromaDB:
    def setup_method(self):
        """Configuration initiale avant chaque test"""
        self.test_collection = "test_collection"
        self.client = get_client("127.0.0.1")

    def teardown_method(self):
        """Nettoyage après chaque test"""
        try:
            delete_collection(self.test_collection)
        except chromadb.errors.InvalidCollectionError:
            # Ignore if collection doesn't exist during cleanup
            pass
        except chromadb.errors.ChromaError as e:
            # Log other ChromaDB-specific errors but don't fail the test
            print(f"Warning: ChromaDB cleanup error: {str(e)}")

    def test_collection_operations(self):
        # Test création collection
        create_collection(self.test_collection)
        
        # Ajouter plus de tests selon les besoins...

    # Ajouter d'autres tests pour ChromaDB... 