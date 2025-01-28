import os
import pytest
from src.llm.functions import (
    file_or_folder,
    create_missing_directories,
    replace_first_folder,
    get_file_extension,
    replace_file_extension,
    create_empty_file
)

class TestFileOperations:
    def setup_method(self):
        """Configuration initiale avant chaque test"""
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)

    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            if os.path.exists(self.test_dir):
                os.rmdir(self.test_dir)

    def test_file_or_folder(self):
        test_file = os.path.join(self.test_dir, "temp_test.txt")
        test_folder = os.path.join(self.test_dir, "temp_folder")
        
        # Créer fichier test
        with open(test_file, "w") as f:
            f.write("test")
        
        # Créer dossier test
        os.makedirs(test_folder, exist_ok=True)
        
        assert file_or_folder(test_file) == "file"
        assert file_or_folder(test_folder) == "folder"
        assert file_or_folder("nonexistent") == "unknow"

    def test_create_missing_directories(self):
        test_path = os.path.join(self.test_dir, "subdir/file.txt")
        create_missing_directories(test_path)
        assert os.path.exists(os.path.dirname(test_path))

    def test_replace_first_folder(self):
        original_path = "docs/subfolder/file.txt"
        new_path = replace_first_folder(original_path, "new_docs")
        assert new_path == os.path.normpath("new_docs/subfolder/file.txt")

    def test_file_extensions(self):
        assert get_file_extension("test.txt") == ".txt"
        assert get_file_extension("test") == ""
        assert get_file_extension("test.tar.gz") == ".gz"
        
        assert replace_file_extension("test.pdf") == "test.txt"
        assert replace_file_extension("test.pdf", ".csv") == "test.csv"
        assert replace_file_extension("folder/") == "folder/"

    def test_create_empty_file(self):
        test_file = os.path.join(self.test_dir, "test_empty.txt")
        create_empty_file(test_file)
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) == 0 