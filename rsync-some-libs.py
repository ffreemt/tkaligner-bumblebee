from pathlib import Path
import subprocess as sp
from logzero import logger

s_dir = Path(rf"\dl\Dropbox\mat-dir\\myapps\tkaligner\.venv\Lib\site-packages").as_posix()

s_dir = f"/cygdrive/c/{s_dir}"

d_dir = Path(r"dl\Dropbox\mat-dir\myapps\pypi-projects\tkaligner-bumblebee\dist\tkaligner-bumblebee").as_posix()
d_dir = f"/cygdrive/c/{d_dir}"

mod_names = [
    "polyglot",
    "pycld2",
    "icu",
    "morfessor",
    "emoji",
    "logzero",
    "torch",
    "laserembeddings",
    "sacremoses",
    "subword_nmt",
    'jieba',
    'transliterate',
    'joblib',
    'tqdm',
    "pandas",
    "pandastable",
    # "tkinter",
    'langid',
    'diskcache',
]

mod_name = "polyglot"
for mod_name in mod_names:
    cmd = f"rsync -uvaz {s_dir}/{mod_name} {d_dir} "
    logger.info(cmd)
    res = sp.check_output(shlex.split(cmd), shell=True)
    logger.info(res.decode("utf8"))
