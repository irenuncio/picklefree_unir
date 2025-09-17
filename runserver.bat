@ECHO OFF
CALL venv\Scripts\activate.bat
python src\manage.py runserver --force-color
