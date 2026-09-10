SELECT
    COUNT(*) AS total_pedidos,
    ROUND(AVG(lead_time_dias), 2) AS lead_time_medio_dias,
    ROUND(
        AVG(CASE WHEN entregue_no_prazo THEN 1.0 ELSE 0.0 END) * 100,
        2
    ) AS otd_percentual,
    ROUND(AVG(valor_pedido), 2) AS valor_medio_pedido,
    ROUND(AVG(nota_avaliacao), 2) AS nota_media
FROM pedidos_logistica;