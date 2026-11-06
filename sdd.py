#!/usr/bin/env python3
"""Entrada de desenvolvimento, sem instalação ou dependências externas."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from sdd_framework.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
