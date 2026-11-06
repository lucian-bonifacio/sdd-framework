#!/usr/bin/env python3
"""Gerar executável zipapp portátil com biblioteca padrão, sem baixar pacotes."""
from __future__ import annotations

import argparse
import shutil
import tempfile
import zipapp
from pathlib import Path


def build(output: Path) -> Path:
    root = Path(__file__).resolve().parents[1]
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sdd-build-") as directory:
        staging = Path(directory)
        shutil.copytree(root / "src/sdd_framework", staging / "sdd_framework", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (staging / "__main__.py").write_text("from sdd_framework.cli import main\nraise SystemExit(main())\n", encoding="utf-8")
        zipapp.create_archive(staging, output, interpreter="/usr/bin/env python3", compressed=True)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist/sdd.pyz"))
    print(build(parser.parse_args().output))
