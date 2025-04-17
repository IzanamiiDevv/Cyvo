@echo off
g++ main.cpp  -o cyvo.exe -I./incl -std=c++17 -lws2_32 -mwindows -static-libgcc -static-libstdc++ -static
