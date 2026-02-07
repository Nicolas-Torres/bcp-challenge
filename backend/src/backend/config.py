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

CONFIG = {
    "open-ai-apikey": os.getenv("OPENAI_API_KEY"),
    "policy": os.path.join(project_root, policy_path),
}
