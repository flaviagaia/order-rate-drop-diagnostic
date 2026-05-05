# order-rate-drop-diagnostic

## Português

`order-rate-drop-diagnostic` é um projeto de diagnóstico de produto inspirado em uma pergunta muito comum em entrevista de marketplace: **o que você faria se a taxa de pedidos caisse de forma relevante?**

O projeto simula duas janelas:

- `baseline`
- `current`

E mostra como decompor a queda usando:

- funil de pedidos;
- região;
- device;
- segmento de usuário.

## Objetivo analítico

Quando a taxa de pedidos cai, a primeira resposta boa não é “rodar um modelo”, e sim:

- medir onde a queda começou;
- localizar quais segmentos mais contribuíram;
- identificar se o problema é topo, meio ou fundo de funil;
- priorizar a primeira hipótese operacional ou de produto.

## O que o projeto faz

1. gera uma base sintética de sessões de funil;
2. compara `baseline` vs `current`;
3. calcula volumes e taxas por etapa do funil;
4. decompõe a queda por:
   - `region`
   - `device`
   - `user_segment`
5. aponta os maiores drivers da queda;
6. devolve uma recomendação inicial de investigação.

## Arquitetura analítica

O projeto trata a queda de pedidos como um problema de **diagnóstico de produto**, não de modelagem preditiva.

O fluxo analítico é:

1. comparar `baseline` e `current`;
2. medir o delta de pedidos;
3. decompor por etapa do funil;
4. decompor por segmento;
5. priorizar a primeira hipótese operacional ou de produto.

## Técnicas utilizadas

- funnel analysis
- period-over-period diagnostic
- segment decomposition
- ranking de drivers de queda
- hipótese orientada por produto

## Contrato dos dados

Cada linha representa uma sessão com campos como:

- `period`
- `region`
- `device`
- `user_segment`
- `promo_shown`
- `app_open`
- `store_view`
- `cart_add`
- `checkout_start`
- `order_placed`

O projeto usa esses flags para reconstruir o funil e comparar a progressão entre janelas.

## Ferramentas e bibliotecas

- `Python`
- `csv`
- `json`
- `pathlib`
- `unittest`

## Resultados esperados do MVP

O projeto foi desenhado para detectar uma queda de pedidos concentrada em:

- `south region`
- e na transição de checkout para pedido concluído

## Resultados atuais

- `baseline_orders = 379`
- `current_orders = 350`
- `order_rate_drop_pct = -7.65`
- maior driver de queda:
  - `south region`

Leitura técnica:

- o topo do funil está relativamente estável;
- a perda aparece com mais força do meio para o fim do funil;
- o `south` concentra a principal deterioração;
- o comportamento por `user_segment` já não está artificialmente enviesado.

## Contrato do relatório

O artefato [order_rate_drop_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/order-rate-drop-diagnostic/data/processed/order_rate_drop_report.json) contém:

- funil do baseline
- funil do current
- taxas por etapa
- decomposição por região
- decomposição por device
- decomposição por segmento
- ranking dos principais drivers
- recomendação inicial de investigação

## Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

## Como defender em entrevista

> Se a taxa de pedidos caisse 10%, eu começaria decompondo a queda por período, etapa do funil e segmentos críticos. Este projeto mostra exatamente esse raciocínio: comparar baseline e current, identificar onde o funil piorou e localizar a queda por região, device e cohort antes de sugerir a primeira hipótese de produto ou operação.
