@echo off
setlocal

git submodule init

if ERRORLEVEL 1 exit /b %ERRORLEVEL%

git submodule update

if ERRORLEVEL 1 exit /b %ERRORLEVEL%

python -m pip install -r "%~dp0\..\heroprotocol\heroprotocol\requirements.txt"

if ERRORLEVEL 1 exit /b %ERRORLEVEL%

python -m pip install -e "%~dp0\..\heroprotocol"

if ERRORLEVEL 1 exit /b %ERRORLEVEL%