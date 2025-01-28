from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain

from src.llm.PromptWithLangchain import set_up_pipeline
from src.service.chromadb.ChromaFunctions import search_in_collection_text


def handling_request(request, path_model, context):
    local_llm = set_up_pipeline(path_model)

    template = PromptTemplate.from_template(
    """
    System: You are a highly accurate and concise assistant. You respond strictly based on the provided context.
    If the context does not contain sufficient information to answer the question, state explicitly: "I do not have enough information in the provided context to answer this question."
    Avoid any invention or assumptions. Always stop your response when the answer is complete, and reply in the language of
    the user's query. Format all output as valid Markdown.

    Context: {context}

    User: {question}

    Assistant:
    """
    )

    data_input = {"question":request, "context":context}
    llm_chain = LLMChain(prompt=template, llm=local_llm)
    response = llm_chain.run(data_input)
    print(response)
    return response
