from pathlib import Path
import subprocess as sp
import shlex

chdir(r"C:\dl\Dropbox\mat-dir\myapps\pypi-projects\tkaligner-bumblebee\tkaligner")

s_dir = "__pycache__"
d_path = r"/cygdrive/c/dl/Dropbox/mat-dir/myapps/pypi-projects/tkaligner-bumblebee/dist/tkaligner-bumblebee"

d_dir = r"C:\dl\Dropbox\mat-dir\myapps\pypi-projects\tkaligner-bumblebee\dist\tkaligner-bumblebee"
d_path1 = Path(d_dir).as_posix().replace("C:", "/cygdrive/c")

# files = Path(s_dir).glob("*.*.pyc")

for file in Path(s_dir).glob("*.*.pyc"):
    file_d = f"{d_path}/{Path(file.stem).stem}{file.suffix}"
    cmd = f"rsync -uvaz {file.as_posix()} {file_d}"
    res = sp.check_output(shlex.split(cmd))
    print(res.decode("utf8"))

# pypi bee_aligner
# C:\dl\Dropbox\mat-dir\myapps\tkaligner\.venv\Lib\site-packages
# polyglot
# icu
# 'pycld2'
# 'morfessor'
# 'pickletools' in C:\Python\Python36\Lib\pickletools.py
# align.ico tkaligner-bumblebee\tkaligner\align.ico

# laserembeddings
# sacremoses