@echo off
py src/quiz.py %1 %2

if %errorlevel% == 9009 (
	echo.
	echo Can't run the game. Python may not be installed on your PC, 
	echo or it is not included on the PATH variable.
)
