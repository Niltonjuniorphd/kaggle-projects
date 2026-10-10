# CLAUDE.md

Repositório de estudos de machine learning com datasets do Kaggle. Cada pasta de primeiro nível é um projeto independente.

## Estrutura

```
kaggle-projects/            # raiz: único repositório git
├── .gitignore              # regras comuns a todos os projetos
├── CLAUDE.md
├── README.md               # propósito do repositório e índice de projetos
└── <projeto>/              # um projeto por dataset/competição
    ├── pyproject.toml      # dependências do projeto (uv)
    ├── uv.lock
    ├── .python-version
    ├── .venv/              # não versionado
    ├── README.md           # link do dataset e instruções de download
    ├── data/               # não versionado (baixado do Kaggle)
    ├── src/scripts/        # scripts de EDA e modelagem
    └── reports/
        ├── report.md       # relatório do projeto
        └── figures/
```

Projetos existentes:

- `arg-river-water/`: classificação da dureza da água de rio ([River Water Parameters](https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data)).

## Versionamento

- O git fica somente na raiz. Não criar `.git` dentro dos projetos (`uv init` cria um por padrão; usar `--vcs none`).
- As pastas `<projeto>/data/` são ignoradas pelo `.gitignore` da raiz. O README de cada projeto deve indicar a fonte e como baixar os dados.
- Mensagens de commit prefixadas com o nome do projeto, por exemplo: `arg-river-water: ajusta pipeline`.

## Ambientes (uv)

Cada projeto tem seu próprio ambiente uv. Não existe workspace nem `pyproject.toml` na raiz.

- Executar os comandos uv **dentro da pasta do projeto**, ou usar `--directory`:
  - `uv sync --directory arg-river-water`
  - `uv add --directory arg-river-water <pacote>`
  - `uv run --directory arg-river-water python src/scripts/model_pipeline.py`
- Nunca adicionar dependências de um projeto em outro.

### Criar um novo projeto

```bash
uv init --vcs none --python 3.14 <projeto>
cd <projeto>
uv add pandas scikit-learn matplotlib seaborn ipykernel
mkdir -p data src/scripts reports/figures
```

Remover o `main.py` gerado pelo `uv init` caso não seja utilizado.

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
