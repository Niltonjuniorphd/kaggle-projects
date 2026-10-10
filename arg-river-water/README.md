# arg-river-water

Classificação da dureza da água de rio (BLANDA / SEMIDURA) a partir de parâmetros físico-químicos medidos em campo.

## Dados

Fonte: [Kaggle – River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data).

Baixar o arquivo `archive.zip` e extraí-lo em `data/archive/`:

```bash
kaggle datasets download natanaelferran/river-water-parameters -p data
unzip data/river-water-parameters.zip -d data/archive
```

## Execução

```bash
uv sync
uv run python src/scripts/model_pipeline.py
```

Relatório: [reports/report.md](reports/report.md).
