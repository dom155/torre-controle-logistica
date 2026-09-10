# 📊 Consultas SQL — Torre de Controle Logística

Esta pasta contém as consultas SQL utilizadas para analisar o desempenho logístico dos pedidos processados pelo projeto.

As análises foram executadas sobre a tabela `pedidos_logistica` no PostgreSQL.

---

## 🤖 Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto, foi utilizada **Inteligência Artificial** como ferramenta de apoio.

A IA auxiliou principalmente em:

- Estruturação e revisão das consultas SQL
- Organização das métricas e indicadores
- Apoio na interpretação inicial dos resultados

Todas as consultas foram **executadas no ambiente PostgreSQL, testadas e validadas durante o desenvolvimento do projeto**.

---

## 01 — KPIs Gerais

Arquivo:

`01_kpis_gerais.sql`

Consulta responsável por apresentar os principais indicadores da operação logística.

### Indicadores obtidos

| Indicador | Resultado |
|---|---:|
| Total de pedidos entregues | 96.470 |
| Lead time médio | 12,56 dias |
| OTD | 91,89% |
| Valor médio do pedido | R$ 159,83 |
| Nota média dos clientes | 4,16 |

### Objetivo

Criar uma visão geral da operação antes de aprofundar a análise por região ou comportamento de entrega.

---

## 02 — Desempenho por Estado

Arquivo:

`02_desempenho_por_estado.sql`

Analisa o desempenho logístico por estado do cliente.

### Métricas analisadas

- Quantidade de pedidos
- Quantidade de pedidos atrasados
- Lead time médio
- OTD
- Nota média dos clientes

### Principais observações

Entre os estados com menor OTD foram identificados:

| Estado | OTD | Lead Time Médio |
|---|---:|---:|
| AL | 76,07% | 24,54 dias |
| MA | 80,33% | 21,57 dias |
| PI | 84,03% | 19,46 dias |
| CE | 84,68% | 21,27 dias |
| SE | 84,78% | 21,52 dias |

O Rio de Janeiro também merece atenção devido ao volume operacional, apresentando OTD de aproximadamente 86,53% e mais de 1.600 pedidos atrasados.

---

## 03 — Atraso x Avaliação do Cliente

Arquivo:

`03_atraso_vs_avaliacao.sql`

Compara os pedidos entregues no prazo com os pedidos entregues após a data estimada.

### Resultados

| Status | Pedidos | Nota Média | Lead Time Médio |
|---|---:|---:|---:|
| No prazo | 88.163 | 4,29 | 10,88 dias |
| Atrasado | 7.661 | 2,57 | 31,38 dias |

Os pedidos atrasados apresentaram atraso médio de aproximadamente **9,45 dias**.

### Insight

A nota média dos clientes caiu de **4,29 para 2,57** nos pedidos atrasados, uma redução de **1,72 ponto**.

Os dados indicam uma forte associação entre atraso logístico e pior experiência do cliente.

---

## 🎯 Perguntas de negócio

As consultas foram desenvolvidas para responder às seguintes perguntas:

1. Qual o percentual de pedidos entregues dentro do prazo?
2. Qual o lead time médio da operação?
3. Quais estados apresentam pior desempenho logístico?
4. Existe relação entre atraso na entrega e avaliação do cliente?

---
