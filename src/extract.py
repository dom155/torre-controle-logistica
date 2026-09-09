from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv"
}


def extract_data():
    datasets = {}

    for name, filename in FILES.items():
        file_path = RAW_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        df = pd.read_csv(file_path)
        datasets[name] = df

        print(
            f"{name}: "
            f"{len(df)} linhas | "
            f"{len(df.columns)} colunas"
        )

    return datasets


if __name__ == "__main__":
    extract_data()