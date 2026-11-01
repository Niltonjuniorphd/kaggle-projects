# argentina-river-water

Classificação da dureza da água de rio (BLANDA / SEMIDURA) a partir de parâmetros físico-químicos medidos em campo.

## Dados

Fonte: [Kaggle – River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data).

Baixar a versão mais recente do dataset em `data/archive/` (a partir da raiz do repositório):

```bash
uv run python argentina-river-water/fetch-data.py
```

## Execução

A partir da raiz do repositório (ambiente uv compartilhado):

```bash
uv sync
uv run python argentina-river-water/src/scripts/model_pipeline.py
```

Relatório: [reports/report.md](reports/report.md).
