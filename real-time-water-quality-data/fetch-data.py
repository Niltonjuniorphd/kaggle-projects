# %%

import sys
from pathlib import Path

# The script lives at the project root (real-time-water-quality-data/)
try:
    PROJECT_ROOT = Path(__file__).resolve().parent
except NameError:
    # Interactive (VS Code / Jupyter) execution from the project root
    PROJECT_ROOT = Path.cwd()

# Make the shared modules in <repository>/src importable
SRC_DIR = str(PROJECT_ROOT.parent / 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from scripts.fetch_function import fetch_dataset  # noqa: E402

import pandas as pd

DATASET_HANDLE = 'ivivan/real-time-water-quality-data'

# %%

# Download the latest dataset version into the project data folder
path = fetch_dataset(DATASET_HANDLE, PROJECT_ROOT)

print('Path to dataset files:', path)

# %%

# List the downloaded files
csv_files = sorted(f for f in path.rglob('*.csv') if f.is_file())
for file in csv_files:
    print(file.relative_to(PROJECT_ROOT))

# %%

# Expected schema (superset of columns across all station CSVs).
# Units, where applicable: Conductivity (uS/cm), NO3 (mg/L), Temp (degC),
# Turbidity (NTU), Level (m), Q (m3/s). Each station file only reports the
# subset of sensors it actually has installed, so columns are optional, but
# any column present must match this dtype.
EXPECTED_DTYPES = {
    'Timestamp': 'str',
    'Q': 'float64',
    'Conductivity': 'float64',
    'NO3': 'float64',
    'Temp': 'float64',
    'Turbidity': 'float64',
    'Level': 'float64',
    'Dayofweek': 'int64',
    'Month': 'int64',
}
REQUIRED_COLUMNS = {'Timestamp', 'Dayofweek', 'Month'}


def validate_schema(df, source_name):
    '''Validate a station dataframe against EXPECTED_DTYPES before concatenation.'''
    columns = set(df.columns)

    missing_required = REQUIRED_COLUMNS - columns
    if missing_required:
        raise ValueError(f'{source_name}: missing required columns {missing_required}')

    unknown_columns = columns - set(EXPECTED_DTYPES)
    if unknown_columns:
        raise ValueError(f'{source_name}: unexpected columns {unknown_columns}')

    for col in columns:
        actual_dtype = str(df[col].dtype)
        expected_dtype = EXPECTED_DTYPES[col]
        if actual_dtype != expected_dtype:
            raise ValueError(
                f'{source_name}: column "{col}" has dtype {actual_dtype}, '
                f'expected {expected_dtype}'
            )


# %%

# Validate each station CSV's schema, then concatenate into a single
# long-format dataframe. Missing sensor columns (e.g. a station without a
# Turbidity probe) become NaN rather than failing validation, since the
# column set is a documented subset of EXPECTED_DTYPES per station.
frames = []
for file in csv_files:
    df = pd.read_csv(file)
    validate_schema(df, file.name)

    station = file.stem.removesuffix('_joined')
    df.insert(0, 'station', station)
    frames.append(df)

all_stations = pd.concat(frames, ignore_index=True, sort=False)
all_stations['Timestamp'] = pd.to_datetime(all_stations['Timestamp'])

print(f'Concatenated {len(csv_files)} stations into {len(all_stations)} rows.')
all_stations.info()

# %%

# Persist the validated, concatenated dataset as a single Parquet file
parquet_path = path / 'all_stations.parquet'
all_stations.to_parquet(parquet_path, index=False)

print('Parquet file written to:', parquet_path.relative_to(PROJECT_ROOT))
