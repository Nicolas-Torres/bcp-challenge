from backend.rag import tool_consult_policies
from backend.config import CONFIG

from crewai import Agent
from langchain_openai import ChatOpenAI

api_key_open_ai = CONFIG["open-ai-apikey"]

llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=api_key_open_ai)

policy_agent = Agent(
    role='Fiscal de Seguridad Bancaria',
    goal='Encontrar patrones sospechosos y evidencias de fraude en la transacción.',
    backstory="""Eres un experto en ciberseguridad detectando fraudes complejos.
    Si una transacción viola una regla escrita, debes reportarlo inmediatamente.""",
    llm=llm,
    tools=[tool_consult_policies],
    verbose=True,
)