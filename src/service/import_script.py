from service.document_service import DocumentService

def main():
    # Création du service avec les paramètres par défaut
    document_service = DocumentService()
    
    # Suppression de la collection existante si nécessaire
    document_service.delete_collection("codedelaroute")
    
    # Création d'une nouvelle collection
    document_service.create_collection("codedelaroute")
    
    # Import du document
    document_service.import_document("./test.txt", "codedelaroute")
    
    # Affichage du contenu de la collection
    contents = document_service.get_collection_contents("codedelaroute")
    if contents:
        print("Contenu de la collection :")
        print(contents)
    
    # Test de recherche
    results = document_service.search_documents("codedelaroute", "exemple", k=3)
    if results:
        print("\nRésultats de la recherche :")
        print(results)

if __name__ == "__main__":
    main()
