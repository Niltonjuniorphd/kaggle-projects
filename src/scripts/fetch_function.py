"""Shared helper to download Kaggle datasets into project data folders."""

from pathlib import Path

import kagglehub


def fetch_dataset(
    handle: str,
    project_dir: str | Path,
    data_dir: str = 'data',
    force_download: bool = True,
) -> Path:
    """Download a Kaggle dataset into a project data folder.

    Args:
        handle: Kaggle dataset handle ('owner/dataset' or
            'owner/dataset/versions/N').
        project_dir: Root folder of the project that receives the data.
        data_dir: Data folder name, relative to project_dir.
        force_download: Download again even if the files already exist,
            keeping the folder on the latest dataset version.

    Returns:
        Path to the folder containing the downloaded files.
    """
    output_dir = Path(project_dir) / data_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    path = kagglehub.dataset_download(
        handle,
        output_dir=str(output_dir),
        force_download=force_download,
    )
    return Path(path)
