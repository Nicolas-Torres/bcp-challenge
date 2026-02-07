import os
import sys
from dotenv import load_dotenv
from pathlib import Path

current_dir = Path(__file__).resolve()
project_root = current_dir.parents[3]
envPath = os.path.join(project_root, '.env')

if not os.path.exists(envPath):
    print(f"No se encuentra el archivo .env en: {envPath}")
    sys.exit(1)

load_dotenv(envPath, override=True)

policy_path = os.getenv("POLICY_FILE_PATH")
vector_store_path = os.getenv("VECTOR_STORE")
database_path = os.getenv("DATABASE")

CONFIG = {
    "open-ai-apikey": os.getenv("OPENAI_API_KEY"),
    "policy-path": os.path.join(project_root, policy_path),
    "vector-store": os.path.join(project_root, vector_store_path),
    "database": os.path.join(project_root, database_path),
}
