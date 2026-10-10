# %%

from pathlib import Path

import kagglehub

# The script lives at the project root (real-time-water-quality-data/)
try:
    PROJECT_ROOT = Path(__file__).resolve().parent
except NameError:
    # Interactive (VS Code / Jupyter) execution from the project root
    PROJECT_ROOT = Path.cwd()

DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATASET_HANDLE = 'ivivan/real-time-water-quality-data'

# %%

# Download the dataset files directly into the project data folder
path = kagglehub.dataset_download(
    DATASET_HANDLE,
    output_dir=str(DATA_DIR),
)

print('Path to dataset files:', path)

# %%

# List the downloaded files
for file in sorted(DATA_DIR.rglob('*')):
    if file.is_file():
        print(file.relative_to(PROJECT_ROOT))