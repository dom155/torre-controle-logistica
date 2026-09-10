SELECT
    CASE
        WHEN entregue_no_prazo = TRUE THEN 'No prazo'
        ELSE 'Atrasado'
    END AS status_entrega,

    COUNT(*) AS total_pedidos,

    ROUND(
        AVG(nota_avaliacao),
        2
    ) AS nota_media,

    ROUND(
        AVG(lead_time_dias),
        2
    ) AS lead_time_medio_dias,

    ROUND(
        AVG(GREATEST(atraso_dias, 0)),
        2
    ) AS atraso_medio_dias

FROM pedidos_logistica

WHERE nota_avaliacao IS NOT NULL

GROUP BY entregue_no_prazo
ORDER BY entregue_no_prazo DESC;