@echo off
C:\msys64\ucrt64\bin\g++.exe -shared -static -static-libgcc -static-libstdc++ -o mylib.dll maincpp.cpp
pause
