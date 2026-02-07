from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma

from backend.config import CONFIG

loader = JSONLoader(file_path=str(CONFIG["policy"]), jq_schema='.[] | "Política: " + .policy_id + " - Regla: " + .rule', text_content=False)
docs = loader.load()

vector_db = Chroma.from_documents(
    documents=docs, 
    embedding=OpenAIEmbeddings(),
    collection_name="bcp_policies"
)

print(docs)