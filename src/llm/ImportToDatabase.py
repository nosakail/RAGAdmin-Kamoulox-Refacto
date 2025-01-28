from service.chromadb.chromafunctions import *
from FileConverter import *
client = get_client("127.0.0.1")

#delete_collection("codedelaroute")
#print("")
#create_collection("codedelaroute")
#print("")
#convert_pdf_to_txt("Codedelaroute.pdf", "codedelaroute.txt")
#print("")
#add_document_txt("./codedelaroute.txt", "codedelaroute")
#add_document_txt("./test.txt", "codedelaroute")
#print("")
#print_contents_of_collection("codedelaroute")

search_in_collection_text("codedelaroute","connard",3)
