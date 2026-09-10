from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "pedidos_logistica.csv"

load_dotenv(BASE_DIR / ".env")


def load_data():
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo processado não encontrado: {PROCESSED_FILE}"
        )

    df = pd.read_csv(PROCESSED_FILE)

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(database_url)

    print(f"Carregando {len(df)} pedidos no PostgreSQL...")

    with engine.begin() as connection:
        connection.exec_driver_sql("TRUNCATE TABLE pedidos_logistica;")

        df.to_sql(
            "pedidos_logistica",
            connection,
            if_exists="append",
            index=False,
            chunksize=1000
        )

    print("Carga concluída com sucesso.")
    print(f"Registros carregados: {len(df)}")


if __name__ == "__main__":
    load_data()