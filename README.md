# order-rate-drop-diagnostic

## Português

### Visão geral

`order-rate-drop-diagnostic` é um projeto de diagnóstico de produto para marketplace focado em investigar quedas relevantes na taxa de pedidos.

O projeto compara:

- `baseline`
- `current`

e decompõe a queda por:

- etapas do funil;
- região;
- device;
- segmento de usuário.

### Objetivo analítico

Quando a taxa de pedidos cai, a primeira resposta boa não é “rodar um modelo”, e sim:

- localizar onde a queda começou;
- medir quais segmentos mais contribuíram;
- decidir se o problema está no topo, meio ou fundo de funil;
- priorizar a primeira hipótese operacional ou de produto.

### Arquitetura analítica

O fluxo é:

1. comparar `baseline` e `current`;
2. medir o delta de pedidos;
3. decompor por etapa do funil;
4. decompor por segmento;
5. priorizar a primeira hipótese investigativa.

### Estrutura dos dados

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

### Técnicas utilizadas

- funnel analysis
- period-over-period diagnostic
- segment decomposition
- ranking de drivers de queda
- hipótese orientada por produto

### Ferramentas e bibliotecas

- `Python`
- `csv`
- `json`
- `pathlib`
- `unittest`

### Contrato do relatório

O artefato [order_rate_drop_report.json](data/processed/order_rate_drop_report.json) contém:

- funil do baseline
- funil do current
- taxas por etapa
- decomposição por região
- decomposição por device
- decomposição por segmento
- ranking dos principais drivers
- recomendação inicial

### Resultados atuais

- `baseline_orders = 379`
- `current_orders = 350`
- `order_rate_drop_pct = -7.65`
- maior driver de queda:
  - `south region`

Leitura técnica:

- o topo do funil está relativamente estável;
- a perda aparece do meio para o fim do funil;
- o `south` concentra a principal deterioração;
- a decomposição por `user_segment` já não está artificialmente enviesada.

### Arquivos principais

- [main.py](main.py)
- [src/data_factory.py](src/data_factory.py)
- [src/modeling.py](src/modeling.py)
- [tests/test_project.py](tests/test_project.py)

### Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```


## English

### Overview

`order-rate-drop-diagnostic` is a marketplace product diagnostic project focused on investigating material drops in order rate.

The project compares:

- `baseline`
- `current`

and decomposes the drop by:

- funnel stage;
- region;
- device;
- user segment.

### Analytical objective

When order rate drops, the first strong response is not “train a model,” but:

- find where the drop started;
- measure which segments contributed most;
- determine whether the issue lives at the top, middle, or bottom of the funnel;
- prioritize the first operational or product hypothesis.

### Analytical architecture

The flow is:

1. compare `baseline` and `current`;
2. measure the order delta;
3. decompose by funnel stage;
4. decompose by segment;
5. prioritize the first investigation path.

### Data structure

Each row represents one session with fields such as:

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

### Techniques used

- funnel analysis
- period-over-period diagnostic
- segment decomposition
- drop-driver ranking
- product-oriented hypothesis generation

### Tools and libraries

- `Python`
- `csv`
- `json`
- `pathlib`
- `unittest`

### Report contract

The artifact [order_rate_drop_report.json](data/processed/order_rate_drop_report.json) contains:

- baseline funnel
- current funnel
- step-level rates
- regional decomposition
- device decomposition
- segment decomposition
- top drop drivers
- initial recommendation

### Current results

- `baseline_orders = 379`
- `current_orders = 350`
- `order_rate_drop_pct = -7.65`
- main driver:
  - `south region`

### Main files

- [main.py](main.py)
- [src/data_factory.py](src/data_factory.py)
- [src/modeling.py](src/modeling.py)
- [tests/test_project.py](tests/test_project.py)

### How to run

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```
