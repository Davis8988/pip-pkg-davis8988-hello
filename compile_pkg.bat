@echo off

:: This script: compiles the python pkg
::  1. Compiles the python pkg
::  2. Asks to install it


set pkgName=davis8988_hello
set repoDir=%~dp0
set setupFile=setup.py
echo.

:: COMPILE PKG
	call :COLOR_PRINT "=== Compiling pkg: %pkgName% ===" "Cyan"

	echo First CD into repo root dir: %repoDir%
	pushd "%repoDir%"
	if %errorlevel% neq 0 echo. && echo Error - Failed to CD into "%repoDir%" && echo. && echo Aborting.. && pause && exit /b 1

	echo Validating env..
	if not exist "%setupFile%" echo. && echo Error - Missing or unreacahble setup.py file at: "%setupFile%" && echo Cannot compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1
	echo OK && echo.
	
	call :COLOR_PRINT "Compiling.." "Yellow"
	
	set compileCmnd=python "%setupFile%" bdist_wheel
	echo Executing: %compileCmnd%
	%compileCmnd%
	if %errorlevel% neq 0 echo. && echo Error - Bad exit code from compiling command && echo Failure during execution of: %compileCmnd% && echo Failed to compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1

	call :COLOR_PRINT "Success - Finished compiling pkg: %pkgName%" "Green"

	echo Cleaning..
	if exist "build\*" echo Removing dir: "%CD%\build" && rmdir /q /s "build"
	if exist "build\*" rmdir /q /s "build"  && REM Sometimes needs to run this command twice..
	if exist "%pkgName%.egg-info\*" echo Removing dir: "%CD%\%pkgName%.egg-info" && rmdir /q /s "%pkgName%.egg-info"
	if exist "%pkgName%.egg-info\*" rmdir /q /s "%pkgName%.egg-info"
	echo.

:: ASK TO INSTALL
	call :COLOR_PRINT "=== Installing pkg: %pkgName% ===" "Cyan"
	CHOICE /C YN /M "Are you sure"
	if %errorlevel% equ 2 echo Aborting.. && pause && exit 1
	echo Continuing with installation
	
	
	


echo.
echo Done.
echo.
pause
exit /b 0





:: Helper Functions

:COLOR_PRINT
set msg=%~1
set colored=%~2
powershell -ExecutionPolicy ByPass -Command "Write-Host '%msg%' -ForegroundColor %colored%"
EXIT /B