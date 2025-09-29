@echo off
echo ===================================================
echo      INICIANDO O EXTRATOR DE TAREFAS AUVO
echo ===================================================

REM Navega para o diretorio do script.
cd /d "%~dp0"

echo Ativando o ambiente virtual...
call .\\venv\\Scripts\\activate

echo Iniciando a aplicacao Flask...
echo Acesse em seu navegador: http://127.0.0.1:5000
python app.py

echo.
echo Encerrando a aplicacao...
pause