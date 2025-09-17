@ECHO OFF
CALL ..\venv\Scripts\activate.bat
CD ..\src
ECHO python manage.py migrate contenttypes
python manage.py migrate contenttypes
ECHO.
ECHO.
ECHO python manage.py migrate auth
python manage.py migrate auth
ECHO.
ECHO.
ECHO python manage.py migrate admin
python manage.py migrate admin
ECHO.
ECHO.
ECHO python manage.py migrate sessions
python manage.py migrate sessions
ECHO.
ECHO.
ECHO python manage.py createsuperuser --username=admin --email=admin@example.com
python manage.py createsuperuser --username=admin --email=admin@example.com
PAUSE
