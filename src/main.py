from transform import transform_data
from load import load_data


def main():
    print("=== TORRE DE CONTROLE LOGÍSTICA ===\n")

    print("1. Executando transformação...")
    transform_data()

    print("\n2. Carregando dados no PostgreSQL...")
    load_data()

    print("\nPipeline concluído com sucesso.")


if __name__ == "__main__":
    main()