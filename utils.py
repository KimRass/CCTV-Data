from pathlib import Path
import shutil


def create_dir(x):
    x = Path(x)
    if x.suffix:
        x.parent.mkdir(parents=True, exist_ok=True)
    else:
        x.mkdir(parents=True, exist_ok=True)


def rm_dir(x):
    shutil.rmtree(x, ignore_errors=True)
