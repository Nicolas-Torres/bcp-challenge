import streamlit as st
import requests
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="BCP - AI Fraud Detection", layout="wide")

st.title("🛡️ BCP - Panel de Control de Fraude (MVP)")
st.markdown("---")

csv_path = Path(__file__).parent / "transactions.csv"

@st.cache_data
def load_transactions(path):
    return pd.read_csv(path)

try:
    df_transactions = load_transactions(csv_path)
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")
    df_transactions = pd.DataFrame()

st.sidebar.header("📂 Escenarios de Prueba")

if not df_transactions.empty:
    selected_tid = st.sidebar.selectbox(
        "Seleccionar Transacción del CSV:",
        options=df_transactions["transaction_id"].tolist()
    )

    row = df_transactions[df_transactions["transaction_id"] == selected_tid].iloc[0]
else:
    st.sidebar.warning("CSV vacío o no encontrado.")
    row = None

st.sidebar.markdown("---")
st.sidebar.subheader("Edición de Datos (Opcional)")

with st.sidebar.form("transaction_form"):
    t_id = st.text_input("Transaction ID", value=row["transaction_id"] if row is not None else "")
    c_id = st.text_input("Customer ID", value=row["customer_id"] if row is not None else "")
    amount = st.number_input("Monto (PEN)", value=float(row["amount"]) if row is not None else 0.0)
    currency = st.text_input("Moneda", value=row["currency"] if row is not None else "PEN")
    country = st.text_input("País", value=row["country"] if row is not None else "")
    channel = st.text_input("Canal", value=row["chanel"] if row is not None else "")
    device = st.text_input("Device ID", value=row["device_id"] if row is not None else "")
    timestamp = st.text_input("Timestamp", value=row["timestamp"] if row is not None else "")
    merchant = st.text_input("Merchant ID", value=row["merchant_id"] if row is not None else "")
    
    submit_button = st.form_submit_button(label="🚀 Evaluar Transacción Seleccionada")


if submit_button:
    payload = {
        "transaction_id": t_id,
        "customer_id": c_id,
        "amount": amount,
        "currency": currency,
        "country": country,
        "chanel": channel,
        "device_id": device,
        "timestamp": timestamp,
        "merchant_id": merchant
    }

    with st.spinner("🕵️ Los agentes están analizando el caso en el backend..."):
        try:
            response = requests.post("http://localhost:8000/transaction", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Visualización de Veredicto
                col1, col2, col3 = st.columns(3)
                with col1:
                    decision = data['decision']
                    color = "green" if decision == "APPROVE" else "orange" if decision == "CHALLENGE" else "red"
                    st.markdown(f"### Veredicto\n## :{color}[{decision}]")
                with col2:
                    st.metric("Confianza", f"{int(data.get('confidence', 0)*100)}%")
                with col3:
                    st.metric("Score de Riesgo", f"{int(data.get('confidence', 0)*100)}/100")

                st.markdown("---")

                # Tabs de información
                tab1, tab2, tab3 = st.tabs(["📢 Cliente", "🔍 Auditoría", "📄 Citas Legales"])
                with tab1:
                    st.info(data['explanation_customer'])
                with tab2:
                    st.warning(data['explanation_audit'])
                    st.write("**Señales detectadas:**")
                    for signal in data.get('signals', []):
                        st.write(f"- {signal}")
                with tab3:
                    for cite in data.get('citations_internal', []):
                        st.code(f"Política: {cite['policy_id']} | Versión: {cite['version']} | Chunk: {cite['chunk_id']}")
            else:
                st.error(f"Error en API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
else:
    st.info("💡 Selecciona un ID del CSV en el menú lateral y presiona el botón para disparar el análisis.")