import json

from backend.database import DB_CONNECTION

from crewai.tools import tool

@tool("consultar_historial_cliente")
def tool_customer_history(customer_id: str):
    """
    Obtiene estadísticas financieras precisas del historial del cliente.
    Devuelve un JSON: 
    - id del cliente
    - gasto promedio habitual
    - rango horario comun
    - paises frecuentes
    - dispositivos conocidos
    """
    query = """
        SELECT 
            usual_amount_avg, 
            usual_hours, 
            usual_countries, 
            usual_devices
        FROM user_profiles
        WHERE customer_id = ?
    """

    customer_behavior = DB_CONNECTION.execute(query, [customer_id]).fetchone()

    if not customer_behavior:
        print(f"Cliente nuevo: {customer_id}. No tiene historial.")
        customer_behavior = (0.0, "UNKNOWN", [], [])

    perfil = {
        "customer_id": customer_id,
        "gasto_promedio_habitual": customer_behavior[0],
        "rango_horario_comun": customer_behavior[1],
        "paises_frecuentes": customer_behavior[2],
        "dispositivos_conocidos": customer_behavior[3],
    }

    return json.dumps(perfil, indent=2)
