@echo off
title Vaguinhas - LinkedIn Auto Apply
setlocal

echo Sincronizando arquivos...
robocopy "\\wsl.localhost\Ubuntu\home\icaro\desenvolvimento\vaguinhas" "C:\vaguinhas" /E /XD ".git" ".claude" "venv" "__pycache__" /NFL /NDL /NJH /NJS >nul

cd /d "C:\vaguinhas"

echo Verificando dependencias...
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias pela primeira vez...
    pip install pyautogui setuptools openai flask-cors flask webdriver-manager selenium pymsgbox
)

echo.
echo ================================
echo   Vaguinhas - LinkedIn Bot
echo ================================
echo.
echo Qual navegador deseja usar?
echo.
echo   1 - Chrome
echo   2 - Firefox
echo.
set /p BROWSER="Digite 1 ou 2: "

if "%BROWSER%"=="1" goto use_chrome
if "%BROWSER%"=="2" goto use_firefox
goto use_firefox

:use_chrome
echo.
echo Fechando Chrome existente...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 3 /nobreak >nul
set VAGUINHAS_BROWSER=chrome
goto start_bot

:use_firefox
echo.
echo Fechando Firefox existente...
taskkill /F /IM firefox.exe >nul 2>&1
taskkill /F /IM firefox.exe >nul 2>&1
timeout /t 5 /nobreak >nul
:wait_firefox
tasklist /FI "IMAGENAME eq firefox.exe" 2>nul | find /I "firefox.exe" >nul
if %errorlevel%==0 (
    echo Aguardando Firefox fechar...
    timeout /t 2 /nobreak >nul
    goto wait_firefox
)
echo Firefox fechado.
set VAGUINHAS_BROWSER=firefox
goto start_bot

:start_bot
echo.
echo Iniciando o bot com %VAGUINHAS_BROWSER%...
python runAiBot.py
pause
