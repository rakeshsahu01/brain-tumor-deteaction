@echo off
REM Start Flask backend on port 5000
cd /d "c:\Users\royal\Downloads\Brain-Tumor-Detection-main\Brain-Tumor-Detection-main"
echo Installing backend dependencies...
py -3.11 -m pip install -q -r requirements.txt
echo.
echo ========================================
echo Starting Flask Backend on port 5000...
echo ========================================
py -3.11 app.py
