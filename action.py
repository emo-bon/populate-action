#!/usr/bin/env python
import os
import tempfile
import pandas as pd
import shutil
from pathlib import Path
from pyedm.gg import get_xlsx


GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
WATER_LOGSHEET_URL = os.getenv("WATER_LOGSHEET_URL")
SEDIMENT_LOGSHEET_URL = os.getenv("SEDIMENT_LOGSHEET_URL")
HARD_LOGSHEET_URL = os.getenv("HARD_LOGSHEET_URL")


if __name__ == "__main__":
    # refresh github workspace
    for entry in os.listdir(GITHUB_WORKSPACE):
        if not entry.startswith("."):
            entry_path = Path(GITHUB_WORKSPACE) / entry
            if os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
            else:
                os.remove(entry_path)

    # add .gitignore
    with open(".gitignore", "w") as f:
        f.write("sema-workspace\n")
    
    # add .README
    with open("README.md", "w") as f:
        f.write(f"# {GITHUB_REPOSITORY}")

    # add logsheets
    for habitat, url in {"water": WATER_LOGSHEET_URL, "sediment": SEDIMENT_LOGSHEET_URL, "hard": HARD_LOGSHEET_URL}.items():
        if not url.startswith("http"):  # url is undefined
            continue

        with tempfile.TemporaryDirectory() as tmpd:
            doc_id = url.split("/")[5]
            path_xlsx = Path(tmpd) / f"{doc_id}.xlsx"
            get_xlsx(path_xlsx, doc_id)
            xlsx = pd.read_excel(path_xlsx, sheet_name=None, dtype=object, keep_default_na=False)  # read without type sniffing
            path_csv = Path(GITHUB_WORKSPACE) / "logsheets" / "raw"
            path_csv.mkdir(parents=True, exist_ok=True)

            for sheet in ("observatory", "sampling", "measured"):
                try:
                    xlsx[sheet].to_csv(path_csv / f'{habitat}_{sheet}.csv', index=False)
                except KeyError:
                    continue
