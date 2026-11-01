# sisagua-gov-br

Análise dos parâmetros básicos de controle da qualidade da água para consumo humano, informados mensalmente pelos responsáveis pelo abastecimento ao SISAGUA (Sistema de Informação de Vigilância da Qualidade da Água para Consumo Humano), do Ministério da Saúde.

## Dados

Fonte: dados abertos do Ministério da Saúde (governo federal), **não** é um dataset do Kaggle. Arquivo de 2026 (CSV separado por `;`, codificação latin1, compactado em ZIP):

<https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SISAGUA/controle_mensal_parametros_basicos_2026_csv.zip>

Para baixar a versão mais recente e gerar `data/data.parquet`, rode a partir da raiz do repositório:

```bash
uv run python sisagua-gov-br/fetch-data.py
```

Cada execução baixa o arquivo de novo e sobrescreve o ZIP e o Parquet em `data/`. A pasta `data/` não é versionada. Para usar outro ano, altere `YEAR` no `fetch-data.py`.

## Execução

O ambiente uv é o compartilhado da raiz. O `dados_susagua.py` lê `data/data.parquet` usando um caminho relativo, então deve ser executado de dentro da pasta do projeto, inclusive no modo interativo do VS Code:

```bash
uv sync
cd sisagua-gov-br
uv run python dados_susagua.py
```
