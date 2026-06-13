@echo off
title A Simple Display TUI

:: 1. Turn on UTF-8 encoding mode natively
chcp 65001 >nul

set "CURRENT_DIR=%~dp0"
if "%CURRENT_DIR:~-1%"=="\" set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

start wt.exe -d "%CURRENT_DIR%" python game.py
