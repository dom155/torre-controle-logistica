DROP TABLE IF EXISTS pedidos_logistica;

CREATE TABLE pedidos_logistica (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),

    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,

    customer_unique_id VARCHAR(50),
    customer_city VARCHAR(100),
    customer_state CHAR(2),

    quantidade_itens INTEGER,
    valor_produtos NUMERIC(12,2),
    valor_frete NUMERIC(12,2),
    nota_avaliacao NUMERIC(4,2),

    lead_time_dias NUMERIC(10,2),
    atraso_dias NUMERIC(10,2),
    entregue_no_prazo BOOLEAN,
    valor_pedido NUMERIC(12,2)
);