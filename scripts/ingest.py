"""
Ingest CSV files into PostgreSQL with automatic type mapping
"""

import os
import pandas as pd
from sqlalchemy import create_engine, types

# -----------------------------
# 1. Database Configuration
# -----------------------------
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "chewy")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "snap_db")

DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# -----------------------------
# 2. CSV Files to Ingest
# -----------------------------
FILES = {
    "snap_application_outcomes": "sample_data/snap_application_outcomes.csv",
    "snap_application_details": "sample_data/snap_application_details.csv"
}

# -----------------------------
# 3. Connect to PostgreSQL
# -----------------------------
engine = create_engine(DB_URI)

# -----------------------------
# 4. Function: map Pandas dtypes to PostgreSQL
# -----------------------------
def map_dtypes(df):
    dtype_mapping = {}
    for col, dt in df.dtypes.items():
        if "int" in str(dt):
            dtype_mapping[col] = types.INTEGER()
        elif "float" in str(dt):
            dtype_mapping[col] = types.Float()
        elif "datetime" in str(dt):
            dtype_mapping[col] = types.TIMESTAMP()
        else:
            dtype_mapping[col] = types.TEXT()
    return dtype_mapping

# -----------------------------
# 5. Ingest CSV files to PostgreSQL
# -----------------------------
for table_name, file_path in FILES.items():
    print(f"\n📥 Ingesting '{table_name}' from '{file_path}'...")
    
    # Load CSV and try to parse date columns
    df = pd.read_csv(file_path)
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    
    # Upload to database with datatype mapping
    df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=map_dtypes(df))
    
    print(f"✅ '{table_name}' uploaded successfully ({df.shape[0]} rows).")

# -----------------------------
# 6. Preview uploaded tables
# -----------------------------
for table_name in FILES.keys():
    preview = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", engine)
    print(f"\nPreview of '{table_name}':")
    print(preview)

print("\nAll files ingested successfully!")
