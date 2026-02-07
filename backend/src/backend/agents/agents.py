from backend.tools.policy_rag_tool import tool_consult_policies
from backend.tools.history_tool import tool_customer_history
from backend.tools.context_tool import tool_analyze_context

from backend.config import CONFIG

from crewai import Agent
from langchain_openai import ChatOpenAI

api_key_open_ai = CONFIG["open-ai-apikey"]

llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=api_key_open_ai)

context_agent = Agent(
    role='Especialista en Riesgo Situacional',
    goal='Evaluar el peligro inmediato de la transacción basado en factores externos como ubicación, hora y cuantía.',
    backstory="""Eres un experto en seguridad operativa bancaria. Tu enfoque es puramente 
    objetivo: no te distraes con el historial del cliente. Si una transacción ocurre a las 3 AM 
    en un país de alto riesgo o por un monto excesivo, disparas las alarmas. Tu misión es 
    identificar si el contexto de la operación facilita un escenario de fraude.""",
    tools=[tool_analyze_context],
    llm=llm, # El ChatOpenAI que definiste antes
    verbose=True,
    allow_delegation=False
)

patterns_agent = Agent(
    role='Analista de Comportamiento del Cliente',
    goal='Detectar anomalías comparando la transacción actual con el historial del usuario.',
    backstory="""Eres un experto en perfiles de consumo. Tu trabajo es responder: 
        "¿Es normal que este cliente haga esta compra?". 
        Si el cliente es nuevo, asume riesgo alto por incertidumbre.
        Si el cliente tiene historial, busca desviaciones en monto (>200% del promedio), 
        ubicación o dispositivo.""",
    tools=[tool_customer_history], 
    llm=llm,
    verbose=True
)

policy_agent = Agent(
    role='Fiscal de Seguridad Bancaria',
    goal='Encontrar patrones sospechosos y evidencias de fraude en la transacción.',
    backstory="""Eres un experto en ciberseguridad detectando fraudes complejos.
    Si una transacción viola una regla escrita, debes reportarlo inmediatamente.""",
    llm=llm,
    tools=[tool_consult_policies],
    verbose=True,
)