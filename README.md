# Kaggle Projects

Repositório de estudos de machine learning com datasets e competições do [Kaggle](https://www.kaggle.com/).

Cada pasta de primeiro nível é um projeto independente, com ambiente próprio, código, relatório e README específico.

## Projetos

| Projeto | Tarefa | Dataset |
|---|---|---|
| [arg-river-water](arg-river-water/) | Classificação da dureza da água de rio | [River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data) |

## Organização

```
kaggle-projects/
├── README.md               # este arquivo
└── <projeto>/
    ├── README.md           # descrição, fonte dos dados e instruções de execução
    ├── pyproject.toml      # dependências do projeto (uv)
    ├── uv.lock
    ├── data/               # dados do Kaggle (não versionados)
    ├── src/scripts/        # EDA e modelagem
    └── reports/            # relatório e figuras
```

- **Versionamento:** um único repositório git na raiz.
- **Ambientes:** cada projeto possui seu próprio ambiente gerenciado pelo [uv](https://docs.astral.sh/uv/).
- **Dados:** não são versionados; o README de cada projeto indica a fonte e como obtê-los.

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Kaggle CLI](https://github.com/Kaggle/kaggle-api) (opcional, para download dos dados)

## Uso

```bash
cd <projeto>
uv sync
uv run python src/scripts/<script>.py
```

Consulte o README de cada projeto para instruções específicas.
