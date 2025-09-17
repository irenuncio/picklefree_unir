@ECHO OFF
CALL ..\venv\Scripts\activate.bat
CD ..\src
ECHO python manage.py makemigrations core
python manage.py makemigrations core
ECHO.
ECHO.
ECHO python manage.py migrate core
python manage.py migrate core
PAUSE
