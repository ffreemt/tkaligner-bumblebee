rsync.exe -uvaz ./ /cygdrive/e/asus-win10-backup/myapps/pypi-projects/tkaligner-bumblebee/ --exclude .git --exclude testvenv --exclude "**/*.pyc" --exclude "**/diskcache" --exclude dist --exclude build --exclude .pytest_cache --exclude .venv --exclude "**/__pycache__"