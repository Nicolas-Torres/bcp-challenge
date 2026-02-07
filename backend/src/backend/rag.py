import os

from backend.config import CONFIG

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_chroma import Chroma

vector_store = CONFIG["vector-store"]

loader = JSONLoader(file_path=str(CONFIG["policy"]), jq_schema='.[] | "Política: " + .policy_id + " - Regla: " + .rule', text_content=False)
docs = loader.load()

if os.path.exists(vector_store):
    print("Cargando politicas desde local ...")
    vector_db = Chroma(
        persist_directory=str(vector_store), 
        embedding_function=OpenAIEmbeddings(api_key=CONFIG["open-ai-apikey"]),
        collection_name="bcp_policies"
    )
else:
    print("Creando nueva db vectorial con las politicas ...")
    vector_db = Chroma.from_documents(
        documents=docs, 
        embedding=OpenAIEmbeddings(api_key=CONFIG["open-ai-apikey"]),
        collection_name="bcp_policies",
        persist_directory=str(vector_store)
    )

print(docs)