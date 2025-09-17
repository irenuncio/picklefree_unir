@ECHO OFF
CALL ..\venv\Scripts\activate.bat
CD ..\src
ECHO Generando archivo puml...
python manage.py generate_puml --file ..\docs\picklefree_models.puml --title picklefree_models --include core auth contenttypes djf_surveys guardian jet admin sessions --add-help --add-legend
PAUSE
