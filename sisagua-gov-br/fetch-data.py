# %%

import urllib.request
from pathlib import Path

import pandas as pd

# The script lives at the project root (sisagua-gov-br/)
try:
    PROJECT_ROOT = Path(__file__).resolve().parent
except NameError:
    # Interactive (VS Code / Jupyter) execution from the project root
    PROJECT_ROOT = Path.cwd()

DATA_DIR = PROJECT_ROOT / 'data'

# SISAGUA open data (Ministério da Saúde): monthly control of basic
# drinking-water parameters, one ZIP (semicolon-separated CSV) per year
YEAR = 2026
URL = (
    'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SISAGUA/'
    f'controle_mensal_parametros_basicos_{YEAR}_csv.zip'
)

ZIP_PATH = DATA_DIR / f'controle_mensal_parametros_basicos_{YEAR}_csv.zip'
PARQUET_PATH = DATA_DIR / 'data.parquet'

# %%

# Download the latest file version (always overwrites the local copy)
DATA_DIR.mkdir(parents=True, exist_ok=True)
urllib.request.urlretrieve(URL, ZIP_PATH)

print('Downloaded:', ZIP_PATH.relative_to(PROJECT_ROOT))

# %%

# Read the CSV inside the ZIP (latin1, ';' separator) and save as Parquet
data = pd.read_csv(
    ZIP_PATH,
    compression='zip',
    encoding='latin1',
    sep=';',
    low_memory=False,
)
data.info()

data.to_parquet(PARQUET_PATH, index=False)

print('Parquet file written to:', PARQUET_PATH.relative_to(PROJECT_ROOT))
