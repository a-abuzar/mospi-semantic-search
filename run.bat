@echo off
echo Starting MOSPI Semantic Search Web Server...
set FLASK_APP=app/app.py
set FLASK_ENV=development
python app/app.py
pause
