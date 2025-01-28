import pytest
from src.service.chromadb.chromafunctions import (
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
        except:
            pass

    def test_collection_operations(self):
        # Test création collection
        create_collection(self.test_collection)
        
        # Ajouter plus de tests selon les besoins...

    # Ajouter d'autres tests pour ChromaDB... 