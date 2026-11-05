#!/usr/bin/env python3
"""Import Google Sites HTML into structured JSON; see MIGRATION.md."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/import_google_sites.py"), run_name="__main__")
