@echo off

py -m pip install -r requirements.txt

echo.
echo please paste your arduino libraries directory:
set /p dir=
echo.

xcopy "arduino-install" "%dir%" /E

echo.
pause