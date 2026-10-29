@echo off
cd /d "%~dp0"
echo Klasor: %cd%
echo.
echo 1) Paket kuruluyor...
py -m pip install --user --upgrade edge-tts
echo.
echo 2) Sesler uretiliyor (ilk seferde 20-40 dk surebilir, pencereyi kapatmayin)...
py ses_uret.py
echo.
echo Islem bitti. Yukaridaki mesajlari kontrol edin.
pause
