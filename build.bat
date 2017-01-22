rmdir dist /s /q
C:\Python27\Scripts\pyinstaller.exe WaveShift.py -F -i ship_big.ico
copy *.png dist
copy *.jpg dist
copy *.ogg dist
copy *.ttf dist
copy *.wav dist
del dist\ship_big.png
move dist WaveShift