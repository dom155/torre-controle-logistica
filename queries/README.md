# 📊 Consultas SQL — Torre de Controle Logística

Esta pasta contém as consultas SQL desenvolvidas para responder às perguntas de negócio definidas para a primeira versão da Torre de Controle Logística.

As consultas são executadas sobre a tabela `pedidos_logistica` no PostgreSQL.

---

## 🤖 Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto, foi utilizada **Inteligência Artificial** como ferramenta de apoio.

A IA auxiliou principalmente na estruturação e revisão das consultas SQL, organização das métricas e apoio na interpretação inicial dos resultados.

Todas as consultas foram executadas no PostgreSQL, testadas e validadas durante o desenvolvimento.

---

# 01 — KPIs Gerais

## ❓ Perguntas de negócio

**Qual o percentual de pedidos entregues dentro do prazo?**

**Qual o lead time médio da operação?**

Arquivo: `01_kpis_gerais.sql`

## 🔎 Query

```sql
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
```

## 📈 Resultado

| Indicador | Resultado |
|---|---:|
| Total de pedidos entregues | 96.470 |
| Lead time médio | 12,56 dias |
| OTD | 91,89% |
| Valor médio do pedido | R$ 159,83 |
| Nota média | 4,16 |

O resultado mostra que **91,89% das entregas ocorreram dentro da data estimada**, com lead time médio de **12,56 dias**.

---

# 02 — Desempenho por Estado

## ❓ Pergunta de negócio

**Quais estados apresentam pior desempenho logístico?**

Arquivo: `02_desempenho_por_estado.sql`

## 🔎 Query

```sql
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
```

## 📈 Resultado

| Estado | OTD | Lead Time Médio |
|---|---:|---:|
| AL | 76,07% | 24,54 dias |
| MA | 80,33% | 21,57 dias |
| PI | 84,03% | 19,46 dias |
| CE | 84,68% | 21,27 dias |
| SE | 84,78% | 21,52 dias |

## 💡 Insight de negócio

Embora Alagoas apresente o menor OTD, analisar apenas o percentual pode esconder impactos operacionais maiores.

O **Rio de Janeiro**, por exemplo, possui OTD de aproximadamente **86,53%**, mas concentra mais de **1.600 pedidos atrasados**.

Isso demonstra a importância de analisar **percentual de atraso juntamente com volume de pedidos**, permitindo identificar regiões que representam maior impacto para a operação.

---

# 03 — Atraso x Avaliação

## ❓ Pergunta de negócio

**Existe relação entre atraso na entrega e avaliação do cliente?**

Arquivo: `03_atraso_vs_avaliacao.sql`

## 🔎 Query

```sql
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
```

## 📈 Resultado

| Status | Pedidos | Nota Média | Lead Time Médio |
|---|---:|---:|---:|
| No prazo | 88.163 | 4,29 | 10,88 dias |
| Atrasado | 7.661 | 2,57 | 31,38 dias |

Os pedidos atrasados apresentaram atraso médio de aproximadamente **9,45 dias**.

## 💡 Insight de negócio

A avaliação média caiu de **4,29 para 2,57** nos pedidos atrasados, uma diferença de **1,72 ponto**.

O resultado mostra uma forte associação entre desempenho logístico e experiência do cliente.

A análise identifica uma **associação**, não sendo suficiente para afirmar causalidade entre atraso e avaliação.

---

## 🎯 Conclusão

As consultas permitem transformar a base processada pelo pipeline ETL em respostas diretamente relacionadas a problemas de negócio.

A combinação entre OTD, lead time, volume regional e avaliação dos clientes permite identificar não apenas onde existem problemas logísticos, mas também onde esses problemas podem gerar maior impacto operacional e na experiência do cliente.