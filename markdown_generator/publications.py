#!/usr/bin/env python3
"""Compatibility entry point. See MIGRATION.md for the current data workflow."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/generate_publications.py"), run_name="__main__")
