# CLAUDE.md

Repositório de estudos de machine learning aplicado à química, com datasets do Kaggle. Cada pasta de primeiro nível é um projeto independente.

## Domínio

Todos os projetos usam dados de análises químicas de amostras ou de experimentos no campo da química.

- Preservar e documentar as unidades de medida (por exemplo, mg CaCO₃/L, µS/cm, mol/L) nos nomes de variáveis, tabelas e gráficos.
- Usar nomenclatura química correta (fórmulas, espécies, parâmetros físico-químicos).
- Avaliar vazamento de informação (data leakage) entre variáveis quimicamente relacionadas, como medidas laboratoriais que definem o alvo.
- Interpretar os resultados dos modelos à luz do contexto químico no `reports/report.md`.

## Estrutura

```
kaggle-projects/            # raiz: único repositório git
├── .gitignore              # regras comuns a todos os projetos
├── CLAUDE.md
├── README.md               # propósito do repositório e índice de projetos
├── pyproject.toml          # dependências de todos os projetos (uv)
├── uv.lock
├── .python-version
├── .venv/                  # ambiente único, não versionado
├── src/scripts/            # módulos compartilhados entre projetos
│   └── fetch_function.py   # fetch_dataset(): download de datasets do Kaggle
└── <projeto>/              # um projeto por dataset/competição
    ├── README.md           # link do dataset e instruções de download
    ├── fetch-data.py       # baixa/atualiza o dataset em data/
    ├── data/               # não versionado (baixado do Kaggle)
    ├── src/scripts/        # scripts de EDA e modelagem
    └── reports/
        ├── report.md       # relatório do projeto
        └── figures/
```

Projetos existentes:

- `arg-river-water/`: classificação da dureza da água de rio ([River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data)).
- `real-time-water-quality-data/`: qualidade da água em tempo real ([Real-time Water Quality Data](https://www.kaggle.com/datasets/ivivan/real-time-water-quality-data)).

## Download dos dados

Cada projeto tem um `fetch-data.py` na sua raiz que importa `fetch_dataset` de `src/scripts/fetch_function.py` e define o handle do Kaggle (`dono/dataset`).

- `fetch_dataset(handle, project_dir, data_dir='data', force_download=True)` baixa o dataset para `<project_dir>/<data_dir>`.
- `force_download=True` por padrão: cada execução baixa novamente a versão mais recente.
- O `fetch-data.py` adiciona `<raiz>/src` ao `sys.path` antes do import (`from scripts.fetch_function import fetch_dataset`).
- Execução: `uv run python <projeto>/fetch-data.py`.

## Versionamento

- O git fica somente na raiz. Não criar `.git` dentro dos projetos.
- As pastas `<projeto>/data/` são ignoradas pelo `.gitignore` da raiz. O README de cada projeto deve indicar a fonte e como baixar os dados.
- Mensagens de commit prefixadas com o nome do projeto, por exemplo: `arg-river-water: ajusta pipeline`.

## Ambiente (uv)

Um único ambiente uv na raiz atende a todos os projetos: `pyproject.toml`, `uv.lock`, `.python-version` e `.venv/` ficam somente na raiz. Os projetos não têm arquivos uv próprios.

- O uv localiza o `pyproject.toml` da raiz a partir de qualquer subpasta; não é necessário ativar ou desativar ambientes ao trocar de projeto.
- Comandos (de qualquer pasta do repositório):
  - `uv sync`
  - `uv add <pacote>`
  - `uv run python arg-river-water/src/scripts/model_pipeline.py`
- No VS Code, usar o interpretador `.venv/bin/python` da raiz.
- Nunca executar `uv init` dentro de um projeto.

### Criar um novo projeto

```bash
mkdir -p <projeto>/{data,src/scripts,reports/figures}
touch <projeto>/README.md <projeto>/reports/report.md
cp real-time-water-quality-data/fetch-data.py <projeto>/   # ajustar DATASET_HANDLE
uv add <pacotes-adicionais>   # somente se necessário
```

Ao criar um projeto, preencher o `README.md` do projeto (descrição, fonte dos dados, execução) e adicionar uma linha na tabela de projetos do `README.md` da raiz.

## Convenções de código

- Python, aspas simples, comentários em inglês.
- Scripts organizados em células `# %%` (execução interativa no VS Code).
- Resolução de caminhos compatível com execução por script e interativa:

```python
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
except NameError:
    # Interactive (VS Code / Jupyter) execution from src/scripts
    PROJECT_ROOT = Path.cwd().parents[1]

DATA_DIR = PROJECT_ROOT / 'data'
FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'
```

- Figuras salvas em `reports/figures/`; resultados e conclusões documentados em `reports/report.md` (em português).
