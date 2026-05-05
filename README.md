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

## Técnicas utilizadas

- funnel analysis
- period-over-period diagnostic
- segment decomposition
- ranking de drivers de queda
- hipótese orientada por produto

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

## Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

## Como defender em entrevista

> Se a taxa de pedidos caisse 10%, eu começaria decompondo a queda por período, etapa do funil e segmentos críticos. Este projeto mostra exatamente esse raciocínio: comparar baseline e current, identificar onde o funil piorou e localizar a queda por região, device e cohort antes de sugerir a primeira hipótese de produto ou operação.
