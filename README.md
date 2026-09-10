# 🚚 Torre de Controle Logística

Pipeline de dados e Business Intelligence para análise de desempenho logístico no e-commerce brasileiro.

O projeto utiliza dados públicos do e-commerce brasileiro da Olist para construir uma análise logística de ponta a ponta, passando por extração, transformação, armazenamento em PostgreSQL, consultas SQL e, posteriormente, visualização em Power BI.

O objetivo é transformar dados brutos de pedidos em indicadores capazes de apoiar decisões relacionadas a prazo de entrega, eficiência operacional e experiência do cliente.

---

## 🎯 Problema de negócio

Em uma operação de e-commerce, apenas acompanhar a quantidade de pedidos não é suficiente.

Atrasos nas entregas podem afetar diretamente a experiência do cliente, enquanto diferenças regionais de desempenho podem indicar gargalos importantes na operação logística.

A proposta deste projeto é construir uma visão analítica capaz de responder:

1. Qual o percentual de pedidos entregues dentro do prazo?
2. Qual o lead time médio da operação?
3. Quais estados apresentam pior desempenho logístico?
4. Existe relação entre atraso na entrega e avaliação do cliente?

---

## 📦 Dataset

Foi utilizado o **Brazilian E-Commerce Public Dataset by Olist**, composto por dados de pedidos realizados em um e-commerce brasileiro.

Para a primeira versão do projeto foram utilizadas quatro bases:

- Pedidos
- Clientes
- Itens dos pedidos
- Avaliações dos clientes

Os arquivos brutos são mantidos apenas no ambiente local e não são versionados no GitHub.

---

## 🏗️ Arquitetura

```text
Dados Olist (CSV)
        ↓
     Extract
        ↓
Python + Pandas
        ↓
    Transform
        ↓
pedidos_logistica.csv
        ↓
      Load
        ↓
   PostgreSQL
        ↓
Consultas SQL
        ↓
    Power BI
```

O pipeline pode ser executado através do arquivo:

```bash
python src/main.py
```

---

## 🔄 Pipeline ETL

### Extract

O arquivo `src/extract.py` é responsável por localizar e carregar os arquivos CSV utilizados pelo projeto.

Durante a execução são validados os arquivos necessários e exibidas informações sobre quantidade de linhas e colunas carregadas.

### Transform

O arquivo `src/transform.py` realiza o tratamento e consolidação dos dados.

Entre as principais transformações estão:

- Conversão das colunas de data
- Agregação dos itens por pedido
- Agregação das avaliações por pedido
- Junção das bases de pedidos, clientes, itens e avaliações
- Filtragem de pedidos efetivamente entregues
- Remoção de registros sem datas essenciais para a análise logística
- Cálculo de lead time
- Cálculo de dias de atraso
- Identificação de entregas dentro do prazo
- Cálculo do valor total do pedido

Após o processamento, a base analítica contém **96.470 pedidos**, mantendo uma linha por pedido e sem duplicidade de `order_id`.

### Load

O arquivo `src/load.py` realiza a conexão com o PostgreSQL e carrega os dados processados na tabela:

```text
pedidos_logistica
```

As credenciais do banco são armazenadas em um arquivo `.env`, que não é versionado no GitHub.

---

## 🗃️ Modelagem dos dados

Nesta primeira versão foi utilizada uma tabela analítica central com granularidade de **um registro por pedido**.

Antes dos `JOINs`, itens e avaliações são agregados por `order_id`.

Essa decisão evita que pedidos contendo vários produtos gerem duplicidade de registros durante a consolidação das bases.

A tabela final reúne informações de:

- Pedido
- Cliente
- Localização por estado
- Quantidade de itens
- Valor dos produtos
- Valor do frete
- Avaliação
- Datas logísticas
- Lead time
- Atraso
- Status de entrega no prazo

---

## 📊 Indicadores encontrados

| Indicador | Resultado |
|---|---:|
| Pedidos analisados | 96.470 |
| Lead time médio | 12,56 dias |
| OTD | 91,89% |
| Valor médio do pedido | R$ 159,83 |
| Nota média dos clientes | 4,16 |

### OTD

O indicador **On-Time Delivery (OTD)** considera como entrega dentro do prazo os pedidos cuja data real de entrega foi menor ou igual à data estimada de entrega.

O resultado geral encontrado foi:

**91,89% dos pedidos entregues dentro do prazo.**

---

## 🌎 Desempenho regional

A análise por estado mostrou diferenças relevantes no desempenho logístico.

Entre os estados com menor OTD:

| Estado | OTD | Lead Time Médio |
|---|---:|---:|
| AL | 76,07% | 24,54 dias |
| MA | 80,33% | 21,57 dias |
| PI | 84,03% | 19,46 dias |
| CE | 84,68% | 21,27 dias |
| SE | 84,78% | 21,52 dias |

Além do percentual de entrega no prazo, o volume precisa ser considerado.

O **Rio de Janeiro**, por exemplo, apresentou OTD de aproximadamente **86,53%**, mas concentrou mais de **1.600 pedidos atrasados**, tornando-se relevante do ponto de vista operacional mesmo sem possuir o pior percentual.

---

## ⭐ Atraso x experiência do cliente

Um dos principais resultados encontrados no projeto foi a diferença de avaliação entre pedidos entregues no prazo e pedidos atrasados.

| Status | Pedidos | Nota Média | Lead Time |
|---|---:|---:|---:|
| No prazo | 88.163 | 4,29 | 10,88 dias |
| Atrasado | 7.661 | 2,57 | 31,38 dias |

Os pedidos atrasados apresentaram atraso médio de aproximadamente:

**9,45 dias**

A nota média caiu de:

**4,29 → 2,57**

uma redução de:

**1,72 ponto**

---

## 💡 Narrativa de negócio

Os resultados indicam que o desempenho logístico não afeta apenas indicadores operacionais.

Pedidos entregues após a data estimada apresentam uma avaliação média significativamente menor do que pedidos entregues dentro do prazo.

Além disso, existem diferenças importantes entre estados, mostrando que uma análise regional pode ajudar a identificar áreas prioritárias para investigação.

Do ponto de vista de negócio, os dados sugerem que ações voltadas à redução de atrasos podem contribuir não apenas para melhorar o OTD, mas também para melhorar a experiência e satisfação do cliente.

---

## 🧠 Decisões técnicas

### Por que Olist?

O dataset foi escolhido por possuir dados brasileiros de e-commerce organizados em múltiplas tabelas relacionadas, permitindo trabalhar com problemas próximos aos encontrados em ambientes reais de dados.

Além disso, possui informações importantes para análise logística, como:

- Data da compra
- Data de entrega
- Previsão de entrega
- Frete
- Estado do cliente
- Avaliação do pedido

### Por que uma linha por pedido?

O `order_id` foi definido como granularidade principal da base analítica.

Como um pedido pode conter vários itens, a base de itens é agregada antes da junção com os pedidos.

Essa abordagem evita duplicidades e torna os indicadores de entrega mais consistentes.

### Por que PostgreSQL?

O PostgreSQL foi utilizado para separar a etapa de processamento em Python da etapa de análise em SQL.

Isso permite simular um fluxo comum em ambientes de dados:

```text
Fonte → ETL → Banco de Dados → Análise → BI
```

### Por que não utilizar geolocalização nesta versão?

A análise inicial utiliza estado e cidade presentes na base de clientes.

A tabela detalhada de geolocalização não foi incorporada à V1 para evitar complexidade desnecessária e possíveis multiplicações de registros durante os relacionamentos.

---

## ⚠️ Limitações

Esta primeira versão possui algumas limitações importantes:

- A análise considera apenas pedidos entregues
- Pedidos sem datas essenciais de entrega foram removidos
- OTD é calculado com base na data estimada originalmente registrada no dataset
- A análise identifica associação entre atraso e avaliação, mas não prova causalidade
- Não são analisados transportadores específicos
- Não existem informações detalhadas sobre centros de distribuição ou rotas
- A análise geográfica está limitada principalmente ao estado do cliente
- Os dados representam um período histórico e não uma operação em tempo real

Essas limitações devem ser consideradas durante a interpretação dos resultados.

---

## 🤖 Uso de Inteligência Artificial

Durante o desenvolvimento foi utilizada **Inteligência Artificial como ferramenta de apoio**.

A IA auxiliou em atividades como:

- Estruturação e revisão de código
- Estruturação e revisão das consultas SQL
- Organização dos indicadores
- Apoio na interpretação inicial dos resultados

As etapas foram executadas, testadas e validadas no ambiente local durante o desenvolvimento.

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)

---

## 📁 Estrutura

```text
torre-controle-logistica/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
│
├── database/
│   └── schema.sql
│
├── queries/
│   ├── 01_kpis_gerais.sql
│   ├── 02_desempenho_por_estado.sql
│   ├── 03_atraso_vs_avaliacao.sql
│   └── README.md
│
├── dashboard/
│   └── screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md
```
