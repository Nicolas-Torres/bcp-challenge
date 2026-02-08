from crewai import Crew, Process, Task
from backend.agents.agents import context_agent, patterns_agent, policy_agent, judge_agent
from pydantic import BaseModel, Field
from typing import List

class InternalCitation(BaseModel):
    policy_id: str = Field(..., description="ID de la política aplicada")
    chunk_id: str = Field(..., description="ID del fragmento recuperado")
    version: str = Field(..., description="Versión de la normativa")

class TransactionVeredict(BaseModel):
    decision: str = Field(..., description="APPROVE, BLOCK o CHALLENGE")
    confidence: float = Field(..., description="Nivel de confianza del 0.0 al 1.0")
    signals: List[str] = Field(..., description="Alertas detectadas")
    citations_internal: List[InternalCitation] = Field(..., description="Citas de políticas")
    explanation_customer: str = Field(..., description="Mensaje para el cliente")
    explanation_audit: str = Field(..., description="Justificación técnica")

def run_fraud_analysis(transaction_data: dict):
    transaction_desc = f"""
    ID: {transaction_data.get('transaction_id')}
    Cliente: {transaction_data.get('customer_id')}
    Monto: {transaction_data.get('amount')} {transaction_data.get('currency')}
    País: {transaction_data.get('country')}
    Timestamp: {transaction_data.get('timestamp')}
    Dispositivo: {transaction_data.get('device_id')}
    Canal: {transaction_data.get('chanel')}
    """

    context_task = Task(
        name="context_agent",
        description=f"Analizar riesgo situacional (monto y horario) de la transacción: {transaction_desc}",
        expected_output="Informe de banderas rojas situacionales.",
        agent=context_agent
    )

    behavioral_task = Task(
        name="patterns_agent",
        description=f"Analizar comportamiento histórico del cliente para la transacción: {transaction_desc}",
        expected_output="Reporte de desviaciones respecto al historial habitual.",
        agent=patterns_agent
    )

    policy_task = Task(
        name="policy_agent",
        description=f"Consultar políticas internas para la transacción: {transaction_desc}",
        expected_output="Referencia normativa aplicable con ID y versión.",
        agent=policy_agent
    )

    verdict_task = Task(
        name="judge_agent",
        description="""Consolidar los informes y emitir el veredicto final.""",
        expected_output="Objeto TransactionVeredict con decisión, señales y citas.",
        agent=judge_agent,
        context=[context_task, behavioral_task, policy_task],
        output_pydantic=TransactionVeredict
    )

    fraud_crew = Crew(
        name="Crew agentes (context, petterns, policy, judge)",
        agents=[context_agent, patterns_agent, policy_agent, judge_agent],
        tasks=[context_task, behavioral_task, policy_task, verdict_task],
        process=Process.sequential,
        verbose=True
    )

    result = fraud_crew.kickoff()
    return result.pydantic.model_dump()

