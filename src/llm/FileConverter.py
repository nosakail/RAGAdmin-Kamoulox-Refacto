import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import csv
import shutil

def _check_file_permissions(source_path: str, save_path: str) -> None:
    """
    Vérifie les permissions des fichiers source et destination.
    
    Raises:
        FileNotFoundError: Si le fichier source n'existe pas
        PermissionError: Si les permissions sont insuffisantes
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Le fichier PDF source {source_path} n'existe pas.")

    if not os.access(source_path, os.R_OK):
        raise PermissionError(f"Impossible de lire le fichier source {source_path}.")

    save_dir = os.path.dirname(save_path) or "."
    if not os.access(save_dir, os.W_OK):
        raise PermissionError(f"Impossible d'écrire dans le dossier de destination {save_dir}.")

def _handle_pdf_error(error: PdfReadError) -> None:
    """
    Gère les erreurs spécifiques au PDF.
    
    Args:
        error: L'erreur PDF à gérer

    Raises:
        PermissionError: Si le PDF est protégé
        ValueError: Si le PDF est corrompu ou vide
        IOError: Pour les autres erreurs de lecture PDF
    """
    error_msg = str(error).lower()
    if "encrypted" in error_msg or "password" in error_msg:
        raise PermissionError("Le fichier PDF est protégé par mot de passe")
    if "file is empty" in error_msg:
        raise ValueError("Le fichier PDF est vide")
    if "file is damaged" in error_msg:
        raise ValueError("Le fichier PDF est endommagé")
    raise IOError(f"Erreur lors de la lecture du PDF: {str(error)}")

def convert_pdf_to_txt(source_path: str, save_path: str) -> None:
    """
    Convertit un fichier PDF en fichier texte en extrayant le contenu de chaque page.

    Cette fonction lit un fichier PDF spécifié par `source_path`, extrait le texte de chaque
    page et l'enregistre dans un fichier texte à l'emplacement `save_path`.

    Args:
        source_path (str): Chemin d'accès au fichier PDF source.
        save_path (str): Chemin où enregistrer le fichier texte généré.

    Raises:
        FileNotFoundError: Si le fichier PDF source n'existe pas.
        PermissionError: Si les permissions sont insuffisantes ou le PDF est protégé.
        IOError: En cas de problème lors de l'écriture du fichier texte.
        ValueError: Si le fichier PDF est vide ou corrompu.

    Example:
        convert_pdf_in_txt("document.pdf", "document.txt")
    """
    _check_file_permissions(source_path, save_path)
    
    try:
        reader = PdfReader(source_path)
        with open(save_path, 'w', encoding='utf-8') as text_file:
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_file.write(text + "\n")
    except (IOError, ValueError) as e:
        raise
    except PdfReadError as e:
        _handle_pdf_error(e)

def convert_csv_to_txt(source_path: str, save_path: str) -> None:
    """
    Convertit un fichier CSV en fichier TXT.

    Args:
        source_path (str): Le chemin du fichier CSV à convertir.
        save_path (str): Le chemin du fichier TXT de sortie.

    Raises:
        FileNotFoundError: Si le fichier source n'existe pas.
        PermissionError: Si les permissions sont insuffisantes pour lire/écrire les fichiers.
        csv.Error: Si une erreur survient lors de la lecture du CSV.
        IOError: Si une erreur survient lors des opérations de fichier.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Le fichier {source_path} n'a pas été trouvé.")

    try:
        with open(source_path, 'r', newline='') as csvfile, \
             open(save_path, 'w', encoding='utf-8') as txtfile:
            try:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    txtfile.write(','.join(row) + '\n')
            except csv.Error as e:
                raise csv.Error(f"Erreur lors de la lecture du CSV: {str(e)}")
    except IOError as e:
        raise IOError(f"Erreur lors des opérations de fichier: {str(e)}")
    except PermissionError as e:
        raise PermissionError(f"Erreur de permissions: {str(e)}")

def copy_file(source: str, destination: str) -> None:
    """
    Copie le contenu d'un fichier source vers un fichier de destination.

    Args:
        source (str): Le chemin du fichier source à copier.
        destination (str): Le chemin du fichier de destination où le contenu sera copié.

    Raises:
        FileNotFoundError: Si le fichier source n'est pas trouvé.
        PermissionError: Si les permissions sont insuffisantes pour lire/écrire les fichiers.
        OSError: Si une erreur système survient lors de la copie (espace disque insuffisant, etc.).
        SameFileError: Si la source et la destination sont le même fichier.

    Exemple:
        copy_file("source.txt", "copie.txt")
        Cette commande copiera le contenu de "source.txt" vers "copie.txt".
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Le fichier source {source} n'existe pas.")

    try:
        shutil.copy2(source, destination)
    except shutil.SameFileError:
        raise shutil.SameFileError(f"La source et la destination sont le même fichier : {source}")
    except PermissionError as e:
        raise PermissionError(f"Permissions insuffisantes pour copier le fichier : {str(e)}")
    except OSError as e:
        raise OSError(f"Erreur système lors de la copie du fichier : {str(e)}")