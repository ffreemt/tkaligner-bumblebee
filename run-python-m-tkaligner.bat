REM need to copy some files to root dir or restructure Page in myapps\tkaligner

REM !cp -i tkaligner\queue1_put.py .
REM !cp -i tkaligner\queues.py .
REM !cp -i tkaligner/myprogressbar1_ui.py .
REM !cp -i tkaligner/myprogressbar_ui_support.py .
REM cp -i tkaligner\check_thread_update.py .
REM cp -i tkaligner\get_time.py .
REM cp -i tkaligner\fetch_queue1.py .

REM start-venv.bat

setlocal PYTHONPATH=tkaligner;%PYTHONPATH%

\dl\Dropbox\mat-dir\\myapps\tkaligner\.venv\Scripts\activate
python -m tkaligner
