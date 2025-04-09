@echo off
g++ main.cpp  -o test.exe -I./incl -std=c++17 -lws2_32 -mwindows -static-libgcc -static-libstdc++ -static
