@ECHO OFF
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d picklefree -f 5_db_show_tables.sql -o "..\docs\picklefree_tables.txt"
PAUSE
