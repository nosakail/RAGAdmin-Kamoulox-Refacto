import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from service.FileConverter import (
    convert_pdf_to_txt,
    convert_csv_to_txt
)
from service.functions import (
    file_or_folder,
    replace_first_folder,
    create_missing_directories,
    replace_file_extension,
    get_file_extension,
    copy_file
)
from service.chromadb.chromafunctions import (
    create_collection,
    add_document_txt,
    delete_a_file_in_the_collection
)



class MyHandler(FileSystemEventHandler):
    """
    Classe qui hérite de FileSystemEventHandler et qui redéfinit les méthodes on_created et on_deleted

    Entrée (str): mirror_folder - le path du dossier miroir
    Sortie : None

    """
    def __init__(self,mirror_folder):
        self.mirror_folder=mirror_folder


    def on_created(self, event):
        path = os.path.normpath(event.src_path)
        if file_or_folder(path) == "file":  # Éviter les dossiers

            mirror_path = replace_first_folder(path,self.mirror_folder)

            create_missing_directories(mirror_path)

            #  convertion du fichier
            # ######################################
            create_collection(Collection_name,Host)
            mirror_path = replace_file_extension(mirror_path)

            new_txt_file = Path(mirror_path)
            if new_txt_file.is_file():
                #print("le fichier existe déjà")
                pass
            else:
                with open(mirror_path, 'w') as new_file:
                    # Crée un fichier vide
                    new_file.write("")

                extension=get_file_extension(path)
                match extension:
                    case ".pdf":
                        print("Conversion du pdf en txt...")
                        convert_pdf_to_txt(path,mirror_path)
                        add_document_txt(mirror_path,Collection_name,Host)
                        #print_contents_of_collection(Collection_name,Host)

                    case ".csv":
                        print("Conversion du csv en txt...")
                        convert_csv_to_txt(path,mirror_path)
                        add_document_txt(mirror_path,Collection_name,Host)

                    case ".txt":
                        print("Copie du txt...")
                        copy_file(path,mirror_path)
                        add_document_txt(mirror_path,Collection_name,Host)
                    case _:
                        print(f"Extension de fichier \"{extension}\" inconnue.")

            # ######################################
        elif file_or_folder(path) == "folder":
            #print(f"Dossier créé : ", path)
            mirror_path = replace_first_folder(path,self.mirror_folder)
            #print(mirror_path)
            create_missing_directories(mirror_path)

        else:
            print("Objet créé inconnu")

    def on_deleted(self, event):
        path = os.path.normpath(event.src_path)

        mirror_path = replace_first_folder(path,self.mirror_folder)
        mirror_path = replace_file_extension(mirror_path) # fichier txt
        file = Path(mirror_path)

        if file.is_file():
            #print(f"Le fichier '{file}' existe.")
            os.remove(mirror_path)

            try:
                delete_a_file_in_the_collection(mirror_path,Collection_name,Host)
            except Exception as e:
                print(f"Erreur, lors de la suppression du fichier dans chroma db : {e}")
            #print_contents_of_collection(Collection_name,Host)
        else:
            if os.path.isdir(mirror_path):# si le dossier existe

                if not os.listdir(mirror_path): #si le dossier est vide
                    os.rmdir(mirror_path)
                else:                          #si le dossier est rempli
                    shutil.rmtree(mirror_path)
            else:
                print(f"Le dossier '{file}' n'existe pas.")


if __name__ == "__main__" :

    # Dossier à surveiller
    PATH_TO_WATCH = "docs"
    PATH_TO_SAVE = "files"

    Host = "192.168.0.22"
    Collection_name = "docs"

    # Initialiser l'observateur
    event_handler = MyHandler(PATH_TO_SAVE)
    observer = Observer()

    # Activer la surveillance récursive
    observer.schedule(event_handler, path=PATH_TO_WATCH, recursive=True)
    try:
        print(f"Surveillance du dossier (et sous-dossiers) : {PATH_TO_WATCH}")
        observer.start()
        while True:
            time.sleep(1)  # Garder le script actif
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
