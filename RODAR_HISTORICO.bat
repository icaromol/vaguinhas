@echo off
title Vaguinhas - Historico de Candidaturas

echo Copiando projeto para Windows...
robocopy "\\wsl.localhost\Ubuntu\home\icaro\desenvolvimento\vaguinhas" "C:\vaguinhas" /E /XD ".git" ".claude" "venv" "__pycache__" /XF "*.bat" /NFL /NDL /NJH /NJS >nul

cd /d "C:\vaguinhas"
echo Iniciando servidor de historico...
start http://localhost:5000
python app.py
pause
