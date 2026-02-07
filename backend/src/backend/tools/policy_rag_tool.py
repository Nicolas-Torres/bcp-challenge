import os

from backend.config import CONFIG

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_chroma import Chroma
from crewai.tools import tool

vector_store = CONFIG["vector-store"]
policy_path = CONFIG["policy-path"]
api_key_open_ai = api_key=CONFIG["open-ai-apikey"]

if os.path.exists(vector_store):
    print("Cargando politicas desde local ...")
    
    vector_db = Chroma(
        persist_directory=str(vector_store), 
        embedding_function=OpenAIEmbeddings(api_key=api_key_open_ai),
        collection_name="bcp_policies"
    )
else:
    print("Creando nueva db vectorial con las politicas ...")

    loader = JSONLoader(file_path=str(policy_path), jq_schema='.[] | "Política: " + .policy_id + " - Regla: " + .rule', text_content=False)
    docs = loader.load()

    vector_db = Chroma.from_documents(
        documents=docs, 
        embedding=OpenAIEmbeddings(api_key=api_key_open_ai),
        collection_name="bcp_policies",
        persist_directory=str(vector_store)
    )

@tool("consult_bcp_policies")
def tool_consult_policies(query: str):
    """
    Útil para consultar las normativas y políticas de fraude del BCP.
    Usa esta herramienta cuando necesites validar si una transacción cumple las reglas.
    Input: Una pregunta o descripción de la transacción (ej: "Monto alto en Tailandia").
    """
    results = vector_db.similarity_search(query, k=3)
    
    return "\n".join([doc.page_content for doc in results])
