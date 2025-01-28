import pytest
import os

@pytest.fixture
def test_dir():
    """Fixture pour créer/nettoyer un répertoire de test"""
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, file))
        os.rmdir(test_dir) 