from pathlib import Path
import pandas as pd

from extract import extract_data

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def transform_data():
    datasets = extract_data()

    orders = datasets["orders"].copy()
    customers = datasets["customers"].copy()
    order_items = datasets["order_items"].copy()
    order_reviews = datasets["order_reviews"].copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(orders[column], errors="coerce")

    items_agg = (
        order_items
        .groupby("order_id", as_index=False)
        .agg(
            quantidade_itens=("order_item_id", "count"),
            valor_produtos=("price", "sum"),
            valor_frete=("freight_value", "sum")
        )
    )

    reviews_agg = (
        order_reviews
        .groupby("order_id", as_index=False)
        .agg(
            nota_avaliacao=("review_score", "mean")
        )
    )

    df = (
        orders
        .merge(
            customers[
                [
                    "customer_id",
                    "customer_unique_id",
                    "customer_city",
                    "customer_state"
                ]
            ],
            on="customer_id",
            how="left"
        )
        .merge(items_agg, on="order_id", how="left")
        .merge(reviews_agg, on="order_id", how="left")
    )

    df = df[df["order_status"] == "delivered"].copy()

    df = df.dropna(
        subset=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    df["lead_time_dias"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    df["atraso_dias"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    df["entregue_no_prazo"] = (
        df["order_delivered_customer_date"]
        <= df["order_estimated_delivery_date"]
    )

    df["valor_pedido"] = (
        df["valor_produtos"].fillna(0)
        + df["valor_frete"].fillna(0)
    )

    df["lead_time_dias"] = df["lead_time_dias"].round(2)
    df["atraso_dias"] = df["atraso_dias"].round(2)
    df["nota_avaliacao"] = df["nota_avaliacao"].round(2)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / "pedidos_logistica.csv"

    df.to_csv(output_file, index=False)

    print("\n--- Transformação concluída ---")
    print(f"Pedidos processados: {len(df)}")
    print(f"Colunas finais: {len(df.columns)}")
    print(f"Pedidos duplicados: {df['order_id'].duplicated().sum()}")
    print(f"Arquivo gerado: {output_file}")

    print("\n--- Indicadores iniciais ---")
    print(f"Lead time médio: {df['lead_time_dias'].mean():.2f} dias")
    print(f"OTD: {df['entregue_no_prazo'].mean() * 100:.2f}%")
    print(f"Avaliações disponíveis: {df['nota_avaliacao'].notna().sum()}")

    return df


if __name__ == "__main__":
    transform_data()