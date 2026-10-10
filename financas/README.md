# Finanças do Bruno

Painel mensal de gastos: https://claude.ai/artifact/WH3SvNcU8wJP9iSpXb7Qe6

- `build_data.py`: transações transcritas de cada mês, categorias, fixo/variável e % de corte sugerido.
- `lancamentos.json`, `meses.json`: gerados pelo script; são as fontes do painel.
- `index.html`: a página do painel (lê as fontes via `dash.data`).

Novo mês: acrescente um bloco em `MESES` no script, rode `python3 financas/build_data.py`
e suba os dois JSON como nova versão das fontes do painel.
