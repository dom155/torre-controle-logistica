SELECT
    customer_state AS estado,
    COUNT(*) AS total_pedidos,

    SUM(
        CASE
            WHEN entregue_no_prazo = FALSE THEN 1
            ELSE 0
        END
    ) AS pedidos_atrasados,

    ROUND(
        AVG(lead_time_dias),
        2
    ) AS lead_time_medio_dias,

    ROUND(
        AVG(
            CASE
                WHEN entregue_no_prazo THEN 1.0
                ELSE 0.0
            END
        ) * 100,
        2
    ) AS otd_percentual,

    ROUND(
        AVG(nota_avaliacao),
        2
    ) AS nota_media

FROM pedidos_logistica

GROUP BY customer_state

ORDER BY
    otd_percentual ASC,
    lead_time_medio_dias DESC;