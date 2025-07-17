@echo off
:start
:: Батник для проверки существования/создания conda-окружения, его активации и запуска сервера 
::(в данном случае на порте 8000, то есть сервак будет локальный)
:: ------------------------------------------------

:: 1. Проверяем наличие conda
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Conda was not found in the PATH
    pause
    exit /b
)

:: 2. Параметры всякие
set ENV_NAME=spam_detector
set PORT=8000
set ENV_FILE=work/scripts/environment.yml

:: 3. Проверяем существование окружения
echo [1/5] Checking environment - %ENV_NAME%...
conda env list | findstr /b /c:"%ENV_NAME%" >nul
if %errorlevel% equ 0 (
    echo [2/5] The environment already exists, skipping this step
    goto ACTIVATE_ENV
) else (
    goto CREATE_ENV
)

:: 4. Создаём окружение (в случае его отсутствия)
:CREATE_ENV
echo [2/5] New environment creating...
conda env create -n %ENV_NAME% -f "%ENV_FILE%" --quiet >nul
if %errorlevel% neq 0 (
    echo Error: Failed to create environment
    pause
    exit /b
)

:: 5. Активируем окружение
:ACTIVATE_ENV
echo [3/5] Environment activation...
call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo Error: Failed to create environment
    pause
    exit /b
)

:: 6. Проверяем наличие всех необходимых файлов
echo [4/5] Components are being checked...
if not exist "work\library\spam_model.pkl" (
    echo Error: Model file spam_model.pkl not found!
    exit /b
)
if not exist "work\library\vectorizer.pkl" (
    echo Error: Vectorizer file vectorizer.pkl not found!
    exit /b
)
if not exist "work\templates\index.html" (
    echo Error: Main page file index.html not found!
    exit /b
)
if not exist "work\templates\settings.html" (
    echo Error: Settings page file settings.html not found!
    exit /b
)
if not exist "work\templates\addinfo.html" (
    echo Error: Working with dataset page file addinfo.html not found!
    exit /b
)
if not exist "work\templates\reports.html" (
    echo Error: Reports page file reports.html not found!
    exit /b
)
if not exist "work\static\style.css" (
    echo Error: Styles file style.css not found!
    exit /b
)
if not exist "work\static\settings.js" (
    echo Error: JS file settings.js not found!
    exit /b
)
if not exist "work\scripts\main.py" (
    echo Error: Fastapi server file main.py not found!
    exit /b
)

:: 7. Запускаем сервак
echo [5/5] Starting the server on port %PORT%...
echo.
echo Docs: http://localhost:%PORT%/docs
echo [CTRL+C] to stop running
echo.

uvicorn work.scripts.main:app --port %PORT% --reload

pause