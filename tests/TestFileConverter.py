import os
import pytest
from pathlib import Path

# Imports spécifiques des fonctions de conversion
from src.llm.FileConverter import (
    convert_pdf_to_txt,
    convert_csv_to_txt,
    copy_file
)

class TestFileConverter:
    def setup_method(self):
        """Configuration initiale avant chaque test"""
        self.test_dir = "test_converter"
        os.makedirs(self.test_dir, exist_ok=True)

    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_copy_file(self):
        source = os.path.join(self.test_dir, "source.txt")
        dest = os.path.join(self.test_dir, "dest.txt")
        
        with open(source, "w") as f:
            f.write("test content")
        
        copy_file(source, dest)
        assert os.path.exists(dest)
        
        with open(dest, "r") as f:
            content = f.read()
        assert content == "test content"

    def test_convert_csv_to_txt(self):
        csv_file = os.path.join(self.test_dir, "test.csv")
        txt_file = os.path.join(self.test_dir, "test_output.txt")
        
        with open(csv_file, "w", newline="") as f:
            f.write("col1,col2\nval1,val2")
        
        convert_csv_to_txt(csv_file, txt_file)
        assert os.path.exists(txt_file)

    def test_error_handling(self):
        with pytest.raises(FileNotFoundError):
            copy_file("nonexistent.txt", "dest.txt")
        
        with pytest.raises(FileNotFoundError):
            convert_csv_to_txt("nonexistent.csv", "output.txt") 