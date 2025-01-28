from langchain_core.tracers.langchain import get_client
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch


def set_up_pipeline(path_model):
    """
    Configure la pipeline pour utiliser le modèle et le tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(path_model)
    model = AutoModelForCausalLM.from_pretrained(path_model)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=100,
        eos_token_id=tokenizer.eos_token_id,
        temperature=0.2,  # Faible température pour réduire l'aléatoire
        top_k=50,  # Restreindre à 50 tokens les plus probables
        top_p=0.9,  # Sélection cumulative des tokens probables
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm, tokenizer, pipe


if __name__ == "__main__":
    try:
        from service.chromadb.ChromaFunctions import *
    except:
        pass

    client = get_client("127.0.0.1")
    collections = client.list_collections()

    print(collections)

    # Vérifier s'il y a au moins une collection
    if collections:
    # Récupérer le nom de la première collection
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='/mnt/sdb/RAGAdmin/LLM/all-mpnet-base-v2')
        first_collection_name = client.get_collection('codedelaroute',embedding_function=sentence_transformer_ef)



    # Définir le nombre de threads pour PyTorch
    torch.set_num_threads(24)

    # Chemin vers le modèle
    modelPath = "../../Meta-Llama-3.1-8B-Instruct"

    # Initialiser le pipeline
    local_llm, tokenizer, pipe = set_up_pipeline(modelPath)

    # Créer un PromptTemplate général
    prompt_template = PromptTemplate.from_template(
        """
        System: You are a helpful assistant. Answer the user's query concisely and clearly. Provide additional structure or formatting (e.g., Markdown) only if explicitly requested by the user.
        Context: {context}
        User: {query}
        Assistant:    
        """
        )

    # Créer une chaîne LLMChain
    llm_chain = LLMChain(prompt=prompt_template, llm=local_llm)

    # Fournir les données comme entrée
    query = "Que faire à un feu rouge ?"
    create_collection("codedelaroute")
    chroma_results = search_in_collection_text("codedelaroute", query, 10)
    input_data = {"query": query, "context": chroma_results}

    # Exécuter la chaîne LangChain et obtenir la réponse
    response = llm_chain.run(input_data)

    # Afficher la réponse avec un print
    print("\n===== Réponse de l'assistant =====\n")
    print(response)
