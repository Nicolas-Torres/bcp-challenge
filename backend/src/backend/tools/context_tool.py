import json
from datetime import datetime
from crewai.tools import tool

PAISES_CRITICOS = ["Tailandia", "Corea del Norte", "Irán", "Rusia", "Islas Caimán"]
HORARIO_CRITICO = { "min_hour": 1,"max_hour": 6 }
MONTO_EXCESIVO = 10000

@tool("analizar_contexto_transaccion")
def tool_analyze_context(amount: float, timestamp: str, country: str):
    """
    Analiza riesgo situacional: monto, hora (madrugada) y reputación del país.
    """
    try:
        dt = datetime.fromisoformat(timestamp)
        hora_24h = dt.hour
        
        alertas = []
        nivel_riesgo = "BAJO"

        if country in PAISES_CRITICOS:
            alertas.append(f"País de alto riesgo detectado: {country}")
            nivel_riesgo = "ALTO"

        if HORARIO_CRITICO["min_hour"] <= hora_24h <= HORARIO_CRITICO["max_hour"]:
            alertas.append(f"Transacción en horario crítico: {hora_24h:02d}h")
            if nivel_riesgo != "ALTO": 
                nivel_riesgo = "MEDIO"

        if amount > MONTO_EXCESIVO:
            alertas.append(f"Monto excede umbral de seguridad: {amount}")
            nivel_riesgo = "ALTO"

        result = {
            "pais_evaluado": country,
            "es_pais_riesgoso": country in PAISES_CRITICOS,
            "nivel_riesgo_contextual": nivel_riesgo,
            "alertas_contexto": alertas
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Error en análisis de contexto: {str(e)}"})