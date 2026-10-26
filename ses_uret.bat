@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py
if "%PY%"=="" (where python >nul 2>nul && set PY=python)
if "%PY%"=="" (
  echo Python bulunamadi. Lutfen python.org adresinden Python kurun ^(kurulumda "Add python.exe to PATH" kutusunu isaretleyin^).
  pause
  exit /b
)
echo Gerekli paket kuruluyor...
%PY% -m pip install --user --upgrade edge-tts
echo.
echo Sesler uretiliyor. Ilk seferde 20-40 dakika surebilir; pencereyi kapatmayin.
%PY% ses_uret.py
echo.
pause
