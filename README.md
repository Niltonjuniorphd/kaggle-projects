# Kaggle Projects

Repositório de estudos de machine learning aplicado à química, com datasets e competições do [Kaggle](https://www.kaggle.com/).

Todos os projetos utilizam dados de análises químicas de amostras ou de experimentos no campo da química (por exemplo, parâmetros físico-químicos de água, composição de materiais, propriedades de compostos).

Cada pasta de primeiro nível é um projeto independente, com ambiente próprio, código, relatório e README específico.

## Projetos

| Projeto | Tarefa | Dataset |
|---|---|---|
| [argentina-river-water](argentina-river-water/) | Classificação da dureza da água de rio | [River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data) |
| [real-time-water-quality-data](real-time-water-quality-data/) | Qualidade da água em tempo real | [Real-time Water Quality Data](https://www.kaggle.com/datasets/ivivan/real-time-water-quality-data) |
| [sisagua-gov-br](sisagua-gov-br/) | Parâmetros básicos de controle da água para consumo humano (2026) | [SISAGUA – Ministério da Saúde](https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SISAGUA/controle_mensal_parametros_basicos_2026_csv.zip) |
| [imp-paulo-notebooks](imp-paulo-notebooks/) | Notebooks de estudo (cap. 3: métodos lineares) | — |

## Organização

```
kaggle-projects/
├── README.md               # este arquivo
├── pyproject.toml          # dependências de todos os projetos (uv)
├── uv.lock
├── src/scripts/            # módulos compartilhados (ex.: download de datasets)
└── <projeto>/
    ├── README.md           # descrição, fonte dos dados e instruções de execução
    ├── fetch-data.py       # baixa/atualiza o dataset do Kaggle em data/
    ├── data/               # dados do Kaggle (não versionados)
    ├── src/scripts/        # EDA e modelagem
    └── reports/            # relatório e figuras
```

- **Versionamento:** um único repositório git na raiz.
- **Ambiente:** um único ambiente [uv](https://docs.astral.sh/uv/) na raiz, compartilhado por todos os projetos.
- **Dados:** não são versionados; cada projeto obtém a versão mais recente com `uv run python <projeto>/fetch-data.py`.

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Kaggle CLI](https://github.com/Kaggle/kaggle-api) (opcional, para download dos dados)

## Uso

```bash
uv sync
uv run python <projeto>/src/scripts/<script>.py
```

Consulte o README de cada projeto para instruções específicas.
