# %%

import sys
from pathlib import Path

# The script lives at the project root (arg-river-water/)
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

DATASET_HANDLE = 'natanaelferran/river-water-parameters'

# %%

# Download the latest dataset version into data/archive,
# the folder read by the EDA and model scripts
path = fetch_dataset(DATASET_HANDLE, PROJECT_ROOT, data_dir='data/archive')

print('Path to dataset files:', path)

# %%

# List the downloaded files
for file in sorted(path.rglob('*')):
    if file.is_file():
        print(file.relative_to(PROJECT_ROOT))
