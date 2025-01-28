import chromadb
from chromadb.utils import embedding_functions
from chromadb.api import EmbeddingFunction
from sentence_transformers import SentenceTransformer
import hashlib
import os


Sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='sentence-transformers/all-mpnet-base-v2')
def stable_hash(file_path):
    """
    Génère un hachage stable basé sur le contenu d'un fichier.
    """
    hasher = hashlib.md5()
    abs_path = os.path.abspath(file_path)

    # Inclure le chemin absolu dans le hachage (facultatif, sinon commenter cette ligne)
    hasher.update(abs_path.encode('utf-8'))

    # Inclure le contenu du fichier dans le hachage
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # Lecture par morceaux pour les fichiers volumineux
            hasher.update(chunk)

    return hasher.hexdigest()

def get_client(ip_host:str = "127.0.0.1",port_of_service=8001):
    try:
        client = chromadb.HttpClient(host=ip_host, port=port_of_service)
    except Exception:
        client = None
    return client

def create_collection(collection_name: str, ip_host: str = "127.0.0.1",port_of_service=8001):
    """
    Vérifie si une collection existe et la crée si elle n'existe pas.

    Args:
        collection_name (str): Nom de la collection à créer ou récupérer.
        ip_host (str): Adresse IP de l'hôte ChromaDB. Par défaut "127.0.0.1".
    """
    # Initialiser la fonction d'embedding

    # Obtenir le client ChromaDB
    client = get_client(ip_host,port_of_service)
    try:
        collection = client.get_collection(collection_name,embedding_function=Sentence_transformer_ef)
        print(f"La collection '{collection_name}' existe déjà. Récupération réussie.")

    except Exception as e:
        try:
            collection = client.create_collection(collection_name, embedding_function=Sentence_transformer_ef)
            print(f"Collection '{collection_name}' créée avec succès.")
        except Exception as ex:
            print(f"Erreur lors de la création ou de la récupération de la collection: {ex}")

def print_contents_of_collection(collection_name: str,ip_host:str = "127.0.0.1",port_of_service=8001):
    client = get_client(ip_host,port_of_service)


    collection = client.get_collection(collection_name, embedding_function=Sentence_transformer_ef)

    all_data = collection.get()  # Récupère tout : ids, documents, metadonnées et embeddings

    # Afficher le contenu
    print("IDs:", all_data["ids"])
    print("Documents:", all_data["documents"])
    print("Metadatas:", all_data["metadatas"])

def delete_collection(collection_name: str,ip_host:str = "127.0.0.1",port_of_service=8001):
    """
    Supprime une collection existante.
    """
    try:
        client = get_client(ip_host,port_of_service)
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' supprimée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection: {e}")

def search_in_collection_text(collection_name: str, query_text: str, k:int=1,ip_host:str = "127.0.0.1",port_of_service=8001):
    """
    Recherche dans la collection en fonction du contenu.
    """
    try:
        client = get_client(ip_host,port_of_service)

        collection = client.get_collection(collection_name, embedding_function=Sentence_transformer_ef)
        results = collection.query(
            query_texts=query_text,
            n_results=k,  # Nombre de résultats à retourner
            include=['documents','metadatas','distances']  # Inclure les documents dans les résultats
        )
        print(f"Résultats de la recherche :")
        print(f"{results}")
        return results
    except Exception as e:
        print(f"Erreur lors de la recherche dans la collection: {e}")
        return None

def search_in_collection_embedding(collection_name: str, query_embedding, k:int=1,ip_host:str = "127.0.0.1",port_of_service=8001):
    """
    Recherche dans la collection en fonction des embeddings.
    """
    try:
        client = get_client(ip_host,port_of_service)

        collection = client.get_collection(collection_name, embedding_function=Sentence_transformer_ef)
        results = collection.query(
            query_embeddings=[query_embedding],  # Embedding de la requête
            n_results=k,  # Nombre de résultats à retourner
            include=['documents']  # Inclure les documents dans les résultats
        )
        print(f"Résultats de la recherche :")
        print(f"{results}")
        return results
    except Exception as e:
        print(f"Erreur lors de la recherche dans la collection: {e}")
        return None

def add_document_txt(txt_path, collection_name, ip_host="127.0.0.1",port_of_service=8001):
    """
    Ajoute un document TXT à une collection. Le contenu est divisé en morceaux (chunks)
    qui se superposent à 10 %, et chaque chunk est ajouté comme un document distinct.
    """
    import os

    try:
        client = get_client(ip_host,port_of_service)

        collection = client.get_collection(collection_name, embedding_function=Sentence_transformer_ef)

        # Charger le contenu du fichier TXT
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"Le fichier {txt_path} est introuvable.")

        with open(txt_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read().strip()

        if not content:
            raise ValueError("Le fichier TXT est vide.")

        # Fonction pour diviser le texte en chunks avec chevauchement
        def split_into_chunks(text, chunk_size, overlap):
            step = chunk_size - overlap
            chunks = []

            for i in range(0, len(text), step):
                chunk = text[i:i + chunk_size]
                if chunk not in chunks:  # Éviter les doublons
                    chunks.append(chunk)

            # Ajouter le reste du texte comme chunk s'il est trop court
            if len(text) > 0 and len(text) % step != 0:
                last_chunk_start = len(text) - chunk_size
                chunks.append(text[max(last_chunk_start, 0):])

            return chunks

        # Définir la taille des chunks et le chevauchement (en caractères)
        chunk_size = 1000  # Taille de chaque chunk (par exemple 1000 caractères)
        overlap = int(chunk_size * 0.1)  # 10 % de chevauchement

        # Diviser le contenu en chunks
        if len(content) <= chunk_size:
            chunks = [content]  # Ajoute tout le texte comme un seul chunk si court
        else:
            chunks = split_into_chunks(content, chunk_size, overlap)

        # Vérifier les IDs existants dans la collection
        existing_ids = set(collection.get()['ids'])

        hash_of_doc = stable_hash(txt_path)
        # Ajouter chaque chunk comme un document avec un ID unique
        for index, chunk in enumerate(chunks):
            doc_id = f"{hash_of_doc}_{index}"

            if doc_id in existing_ids:
                print(f"Le chunk {doc_id} existe déjà dans la collection.")
            else:
                collection.add(
                    ids=[doc_id],
                    documents=[chunk],
                    metadatas=[{"source": txt_path, "chunk_index": index}]
                )
                print(f"Chunk ajouté : {doc_id} ({index + 1}/{len(chunks)})")

        print(f"Document '{txt_path}' divisé en {len(chunks)} chunks et ajouté avec succès à la collection '{collection_name}'.")

    except Exception as e:
        print(f"Une erreur a eu lieu : {e}")


def delete_a_file_in_the_collection(txt_path: str, collection_name: str, ip_host: str = "127.0.0.1",port_of_service=8001):
    """
    Supprime les documents contenant une référence au chemin (txt_path) dans leur contenu brut.

    Args:
        txt_path (str): Le chemin ou texte à rechercher dans le contenu des documents.
        collection_name (str): Le nom de la collection où chercher et supprimer le fichier.
        ip_host (str): L'adresse de l'hôte ChromaDB. Par défaut "127.0.0.1".
    """
    # Connexion au client ChromaDB
    client = get_client(ip_host,port_of_service)

    collection = client.get_collection(collection_name, embedding_function=Sentence_transformer_ef)
    all_documents = collection.get()
    #print("Structure complète de all_documents :", all_documents,"\n")
    # Récupérer tous les documents de la collection
    tab_of_ids = []
    try:
        if "metadatas" in all_documents:
            for index, doc in enumerate(all_documents["metadatas"]):
                print(doc)
                source = doc.get("source")
                if source:
                    print(f"Source : {source}")
                    print(f"Path   : {txt_path}")
                    if source == txt_path:
                        tab_of_ids.append(index)
                else:
                    print("Aucune source trouvée dans ce document.")
        else:
            print("Aucune metadatas trouvée.")

        if len(tab_of_ids)>0:
            if "ids" in all_documents:
                for index, doc_id in enumerate(all_documents["ids"]):
                    print(doc_id)
                    for i in range(len(tab_of_ids)):
                        if tab_of_ids[i]==index:
                            collection.delete(ids=[doc_id])
                            print("Document ",doc_id, " supprimé")
        else:
            print("Aucun document à supprimer")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression du document : {e}")





if __name__ == "__main__":
    Collection_name = "codedelaroute"
    add_document_txt("codedelaroute.txt",Collection_name)
