@ECHO OFF
CALL ..\venv\Scripts\activate.bat
CD ..\src
FOR %%i in (core\fixtures\*.json) DO python manage.py loaddata %%i
PAUSE
