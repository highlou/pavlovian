:: Created 2026-04-25.

@echo off

:: Install the dependencies.
pip install -r requirements.txt

:: Also install PyInstaller.
pip install pyinstaller

:: Build roaster.exe.
pyinstaller -w -F --distpath . pavlovian.py -n pavlovian
