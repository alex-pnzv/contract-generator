@echo off
pyinstaller --onefile --noconsole --icon=exe.ico main.py
pyinstaller --onefile --name debug --icon=exe.ico main.py
iscc /q .\install\install2.iss
pause