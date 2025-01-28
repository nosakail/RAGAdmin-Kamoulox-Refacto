import os
from pypdf import PdfReader
import csv
import shutil

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
        IOError: En cas de problème lors de l'écriture du fichier texte.
        Exception: Pour toute autre erreur inattendue.

    Example:
        convert_pdf_in_txt("document.pdf", "document.txt")
    """
    # Typage explicite des variables
    source_path: str
    save_path: str
    reader: PdfReader
    text: str
    page_num: int
    os.chmod(source_path, 0o777)
    if not os.access(source_path, os.R_OK):
        print(f"Erreur : Impossible de lire le fichier source {source_path}. Vérifiez les permissions.")
        return

    if not os.access(os.path.dirname(save_path) or ".", os.W_OK):
        print(f"Erreur : Impossible d'écrire dans le dossier de destination {os.path.dirname(save_path)}.")
        return

    try:
        # Charger le fichier PDF
        reader = PdfReader(source_path)

        # Ouvrir le fichier texte en mode écriture
        with open(save_path, 'w', encoding='utf-8') as text_file:
            for page_num, page in enumerate(reader.pages, start=1):
                # Extraire le texte de la page
                text = page.extract_text()
                if text:
                    text_file.write(text + "\n")

                # Ajouter une ligne vide entre les pages pour lisibilité
                text_file.write("\n")

        print(f"Conversion réussie ! Le fichier texte a été enregistré sous : {save_path}")
    except Exception as e:
        e: Exception  # Exception capturée
        print(f"Erreur lors de la conversion : {e}")

def convert_csv_to_txt(source_path: str, save_path: str) -> None:
    """
    Convertit un fichier CSV en fichier TXT.

    Args:
        source_path (str): Le chemin du fichier CSV à convertir.
        save_path (str): Le chemin du fichier TXT de sortie.

    Raises:
        FileNotFoundError: Si le fichier source n'existe pas.
        Exception: Pour toute autre erreur inattendue.

    Exemple:
        csv_to_txt("fichier.csv", "fichier.txt")
        Cette commande convertira le fichier "fichier.csv" en "fichier.txt".
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Le fichier {source_path} n'a pas été trouvé.")

    try:
        with open(source_path, 'r', newline='') as csvfile, \
             open(save_path, 'w', encoding='utf-8') as txtfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                txtfile.write(','.join(row) + '\n')
    except Exception as e:
        raise Exception(f"Une erreur est survenue lors de la conversion: {str(e)}")

def copy_file(source: str, destination: str) -> None:
    """
    Copie le contenu d'un fichier source vers un fichier de destination.

    Args:
        source (str): Le chemin du fichier source à copier.
        destination (str): Le chemin du fichier de destination où le contenu sera copié.

    Raises:
        FileNotFoundError: Si le fichier source n'est pas trouvé.
        Exception: Si une autre erreur se produit lors de la copie du fichier.

    Exemple:
        copy_file("source.txt", "copie.txt")
        Cette commande copiera le contenu de "source.txt" vers "copie.txt".
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Le fichier source {source} n'existe pas.")

    try:
        shutil.copy2(source, destination)
    except Exception as e:
        raise Exception(f"Erreur lors de la copie du fichier : {str(e)}")