# Sistema Multi-Agente para Detección de Fraude Ambiguo en Transacciones Financieras

Este proyecto es un MVP de un sistema de detección de fraude en transacciones financieras. Utiliza un enfoque de múltiples agentes de IA para analizar transacciones desde diferentes perspectivas y emitir un veredicto consolidado.

## Arquitectura

El proyecto está estructurado como un monorepo utilizando **uv** como gestor de paquetes y entorno virtual, con dos componentes principales en su workspace:

-   **`/backend`**: Una API construida con **FastAPI** que expone un endpoint para el análisis de transacciones. La lógica central reside en un equipo de agentes de IA orquestado por **CrewAI**.
-   **`/frontend`**: Una aplicación web de panel de control construida con **Streamlit**. Permite a los usuarios enviar transacciones de prueba al backend y visualizar el análisis y veredicto de los agentes.

## Estructura del Workspace

```
/
├── backend/        # Workspace del backend (FastAPI + CrewAI)
├── frontend/       # Workspace del frontend (Streamlit)
├── .gitignore
├── pyproject.toml  # Configuración raíz de uv
└── README.md
```

## Instalación

1. Asegúrate de tener [**uv**](https://github.com/astral-sh/uv) instalado.
    ```
    pip install uv
    ```

1.  Clona el repositorio.
2.  Variables de entorno necesarias:
    ```
    OPENAI_API_KEY=
    POLICY_FILE_PATH=
    VECTOR_STORE=
    DATABASE=
    ```

2.  Desde el directorio raíz del proyecto, ejecutar:

    ```bash
    uv sync
    ```

## Ejecutar el Proyecto

1.  **Iniciar el Backend**:

    Desde la raíz del proyecto abre una terminal y ejecuta:

    ```bash
    uv run uvicorn backend.main:app --reload --port 8000
    ```
    Abrir `http://localhost:8000`.

2.  **Iniciar el Frontend**:

    Desde la raíz del proyecto abre una segunda terminal y ejecuta:

    ```bash
    uv run streamlit run frontend/src/frontend/main.py
    ```
    Se abrirá un navegador automaticamete, apuntando al backend local.

3. **Prueba de Transacciones**: 
    
    Una vez ambos servicios estén activos, usar el panel de control del frontend para seleccionar y enviar transacciones de prueba.
