from pathlib import Path
import subprocess as sp
import shlex
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
    # "pandas",
    # "pandastable",
    'langid',
    'diskcache',
    # 'blinker',
    'dateutil',
    'pytz',
    # 'six.py',
    'sentence_splitter',
    'regex',
    # 'matplotlib',
    # 'pyparsing.py',
    # 'cycler.py',
    # 'kiwisolver',
    'yaspin',
    'yaspin',
]

# mod_names = [
# ]

logger.info(mod_names)

for mod_name in mod_names:
    cmd = f"rsync -uvaz {s_dir}/{mod_name} {d_dir} "
    logger.info(cmd)
    res = sp.check_output(shlex.split(cmd), shell=True)
    # logger.info(res.decode("utf8"))

# """
s_dir1 = Path(rf"\Python\Python36\Lib\site-packages").as_posix()
s_dir1 = f"/cygdrive/c/{s_dir1}"
mod_names = [

]
for mod_name in mod_names:
    cmd = f"rsync -uvaz {s_dir1}/{mod_name} {d_dir} "
    logger.info(cmd)
    res = sp.check_output(shlex.split(cmd), shell=True)
    logger.info(res.decode("utf8"))
# """

s_dir2 = Path(rf"\Python\Python36\lib").as_posix()
s_dir2 = f"/cygdrive/c/{s_dir2}"
mod_names = [
    "tkinter",
    # 'sqlite3',
]
for mod_name in mod_names:
    cmd = f"rsync -uvaz {s_dir2}/{mod_name} {d_dir} "
    logger.info(cmd)
    res = sp.check_output(shlex.split(cmd), shell=True)
    logger.info(res.decode("utf8"))
