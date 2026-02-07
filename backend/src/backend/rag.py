import os

from backend.config import CONFIG

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_chroma import Chroma

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
