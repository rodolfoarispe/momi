@echo OFF
SET original_dir=%CD%
CD C:\Analitica\Programa
SET venv_root_dir=C:\Analitica\myPython
ECHO "ACTIVANDO EL AMBIENTE VIRTUAL"
CALL C:\Users\vpnpower\AppData\Local\Continuum\miniconda3\Scripts\activate.bat %venv_root_dir% 
START python wsgi.py
START chrome --new_window "127.0.0.1:1000"
