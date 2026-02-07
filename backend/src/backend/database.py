import duckdb
import sys
from backend.config import CONFIG

DATABASE = None

def initialize_db():
    """
    Inicializa la conexión a DuckDB y carga los datos CSV en memoria RAM.
    Se asegura de hacerlo solo una vez.
    """
    global DATABASE
    
    if DATABASE is not None:
        return DATABASE

    try:
        csv_path = CONFIG["database"] # Recuerda corregir el typo 'batabase' en tu config
        
        con = duckdb.connect(database=':memory:')
        
        print(f"Cargando datos desde: {csv_path}")
        con.execute(f"CREATE TABLE user_profiles AS SELECT * FROM read_csv_auto('{csv_path}')")
        
        DATABASE = con
        return DATABASE

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

DB_CONNECTION = initialize_db()