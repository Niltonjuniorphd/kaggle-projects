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

DATASET_HANDLE = 'ivivan/real-time-water-quality-data'

# %%

# Download the latest dataset version into the project data folder
path = fetch_dataset(DATASET_HANDLE, PROJECT_ROOT)

print('Path to dataset files:', path)

# %%

# List the downloaded files
for file in sorted(path.rglob('*')):
    if file.is_file():
        print(file.relative_to(PROJECT_ROOT))
