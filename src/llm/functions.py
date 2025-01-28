import os
from pathlib import Path


def file_or_folder(path: str) -> str:
    """
    Fonction qui prends en parametre un chemin d'accès et différencie un fichier d'un dossier

    Entrée : path

    Sortie : folder  -  type d'objet désigné
          ou file
          ou unknow
    """
    # Vérifier si le chemin est un dossier
    if os.path.isdir(path):
        return "folder"
    # Vérifier si le chemin est un fichier
    if os.path.isfile(path):
        return "file"
    return "unknow"


def create_missing_directories(path: str) -> None:
    """
    Crée tous les répertoires manquants dans le chemin donné.

    Entrée: path - Le chemin d'accès pour lequel les répertoires manquants doivent être créés.
    Sortie: None

    """

    path = os.path.normpath(path)
    folder_path = Path(os.path.dirname(path))
    folder_path.mkdir(parents=True, exist_ok=True)


def replace_first_folder(path: str, file_name: str) -> str:
    """
    Fonction qui remplace le premier dossier d'un chemin d'accès par un autre
    Entrée: path - Le chemin d'accès original.
    Sortie: path - nouveau chemin.
    """
    path = os.path.normpath(path)
    dossiers = path.split(os.sep)

    if dossiers[0] != ".":
        dossiers[0] = file_name
    return os.path.join(*dossiers)


def get_file_extension(filename: str) -> str:
    """
    Renvoie l'extension d'un fichier.

    Args:
        filename (str): Le nom du fichier ou son chemin complet.

    Returns:
        str: L'extension du fichier (par exemple '.txt'), ou une chaîne vide si aucune extension.
    """
    _, extension = os.path.splitext(filename)
    return extension


def replace_file_extension(file_path: str, extension: str = ".txt") -> str:
    """
    Remplace l'extension d'un fichier par l'extension spécifiée.

    Args:
        file_path (str): Chemin d'accès au fichier.
        extension (str): Nouvelle extension du fichier (par défaut '.txt').

    Returns:
        str: Nouveau chemin avec l'extension spécifiée, ou le chemin d'origine si une erreur se produit.
    """
    try:
        # If the path ends with a directory separator, return it as is
        if file_path.endswith('/') or file_path.endswith('\\'):
            return file_path
            
        # Get the base path without extension
        base_path = os.path.splitext(file_path)[0]
        
        # Ensure the extension starts with a dot
        if not extension.startswith('.'):
            extension = '.' + extension
            
        return base_path + extension
    except Exception as e:
        print(f"Erreur lors du remplacement de l'extension : {str(e)}")
        return file_path


def create_empty_file(file_path: str) -> None:
    """
    Fonction qui crée un fichier vide (txt par défaut)
    Entrée :
        str : path du fichier à créer

    Sortie : None
    """
    with open(file_path, 'w') as new_file:
        # Crée un fichier vide
        new_file.write("")
