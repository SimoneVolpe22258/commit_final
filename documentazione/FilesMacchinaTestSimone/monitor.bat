rem ******************************************************
rem * Programma batch per avvio ambiente virtuale python *
rem * su pc aziendale dei test.   Simo 23/05/2026        *
rem ******************************************************
echo on
cd\
call c:/scripts/cura.bat
call c:/venv/commit_final/Scripts/activate.bat
cd /d C:\scripts\volpe_simone_commit_final\commit_final\src

python monitor.py
echo off
