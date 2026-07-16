@echo off
echo ==========================================
echo MOSPI Semantic Search - Automated Setup
echo ==========================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies.
    pause
    exit /b %errorlevel%
)
echo.

echo [2/3] Parsing NCO PDFs...
python parser.py
if %errorlevel% neq 0 (
    echo Error during parsing.
    pause
    exit /b %errorlevel%
)
echo.

echo [3/3] Building AI Engine and FAISS Index...
echo (This may take a while depending on your hardware as it downloads the E5 model)
python engine.py
if %errorlevel% neq 0 (
    echo Error during engine build.
    pause
    exit /b %errorlevel%
)
echo.

echo Setup completed successfully!
echo You can now start the application by running run.bat
pause
