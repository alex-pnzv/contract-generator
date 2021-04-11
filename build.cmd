@echo off
create-version-file metadata.yml --outfile file_version_info.txt --version %1
pyinstaller --onefile --noconsole --icon=exe.ico main.py --version-file file_version_info.txt
REM pyinstaller --onefile --name debug --icon=exe.ico main.py
pyinstaller --onefile --noconsole updater.py 
python uploader.py %1 %2 %3
iscc /q .\install\install.iss /DApplicationVersion=%1
pause