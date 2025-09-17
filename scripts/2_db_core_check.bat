@ECHO OFF
CALL ..\venv\Scripts\activate.bat
CD ..\src
ECHO python manage.py check core
python manage.py check core
PAUSE
