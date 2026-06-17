@echo off
echo Procurando Chrome instalado...
echo.

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [ENCONTRADO] C:\Program Files\Google\Chrome\Application\chrome.exe
) else (
    echo [NAO ENCONTRADO] Program Files
)

if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [ENCONTRADO] C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else (
    echo [NAO ENCONTRADO] Program Files x86
)

if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    echo [ENCONTRADO] %LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
) else (
    echo [NAO ENCONTRADO] LocalAppData
)

echo.
echo Procurando em WindowsApps (Microsoft Store)...
dir "%LOCALAPPDATA%\Microsoft\WindowsApps\chrome.exe" 2>nul && echo [ENCONTRADO] WindowsApps || echo [NAO ENCONTRADO] WindowsApps

echo.
pause
