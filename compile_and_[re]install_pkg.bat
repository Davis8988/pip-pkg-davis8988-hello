@echo off
setlocal EnableDelayedExpansion

:: This script: compiles the python pkg
::  1. Compiles the python pkg
::  2. Asks to install it
::
:: Params:
::  1 - Build Version  (Overided by env: 'JENKINS_BUILD_VERSION')
::

set pkgName=davis8988_hello
set repoDir=%~dp0
set setupFile=setup.py
set buildVersion=%~1
set vritualEnvDirName=venv
if not defined buildVersion set buildVersion=1.5
echo.

:: COMPILE PKG
	call :COLOR_PRINT "=== Compiling pkg: %pkgName% ===" "Cyan"

	echo First CD into repo root dir: %repoDir%
	pushd "%repoDir%"
	if %errorlevel% neq 0 echo. && call :COLOR_PRINT "Error - Failed to CD into: %repoDir%" "RED" && echo. && echo Aborting.. && pause && exit /b 1

	echo Validating env..
	if not exist "%setupFile%" echo. && call :COLOR_PRINT "Error - Missing or unreacahble setup.py file at: %setupFile%" "RED" && echo Cannot compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1
	where python >nul 2>&1 || echo. && call :COLOR_PRINT "Error - Missing python.exe from system-path" "RED" && echo Did you install python? && echo Cannot compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1
	echo OK && echo.
	
	call :COLOR_PRINT "Setting pkg version env:" "Yellow"
	call :COLOR_PRINT " LOCAL_BUILD_VERSION=%buildVersion%" "Yellow"
	set LOCAL_BUILD_VERSION=%buildVersion%
	
	echo. && call :COLOR_PRINT "Compiling.." "Yellow"
	set compileCmnd=python "%setupFile%" bdist_wheel
	echo. && echo Executing: %compileCmnd% && echo.
	%compileCmnd%
	if %errorlevel% neq 0 echo. && call :COLOR_PRINT "Error - Bad exit code from compiling command"  "RED" && echo Failure during execution of: %compileCmnd% && echo Failed to compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1

	call :COLOR_PRINT "Success - Finished compiling pkg: %pkgName%" "Green"

	echo Cleaning..
	if exist "build\*" echo Removing dir: "%CD%\build" && rmdir /q /s "build"
	if exist "build\*" rmdir /q /s "build"  && REM Sometimes needs to run this command twice..
	if exist "%pkgName%.egg-info\*" echo Removing dir: "%CD%\%pkgName%.egg-info" && rmdir /q /s "%pkgName%.egg-info"
	if exist "%pkgName%.egg-info\*" rmdir /q /s "%pkgName%.egg-info"
	echo.

:: ASK TO INSTALL
	call :COLOR_PRINT "=== Installing pkg: %pkgName% ===" "Cyan"
	echo Validating env..
	if not exist "dist\*.whl" echo. && call :COLOR_PRINT "Error - Missing or unreachable install pkg wheel file at: %CD%\dist" "RED" && echo Cannot install pkg: %pkgName% && echo. && echo Aborting.. && pause && exit /b 1
	
	
	:: Check wheel file is present after the compile
	echo Continuing with installation
	echo Looking for install pkg wheel file
	set wheelFile=
	for /f %%a in ('dir /b dist\*.whl') do (set wheelFile=%%a)  && REM  Built-in sorting ensures the latest whl file is installed
	if not defined wheelFile echo. && call :COLOR_PRINT "Error - Failed to define var: wheelFile with name of pkg wheel file at: %CD%\dist\*.whl" "RED" && echo Cannot install pkg: %pkgName% && echo. && echo Aborting.. && pause && exit /b 1
	echo Found. && echo.
	echo Install package from wheel file: %CD%\dist\!wheelFile!
	CHOICE /C YN /M "Are you sure"
	if %errorlevel% equ 2 echo Aborting.. && pause && exit 1
	
	
	:: Create Virtual Environment
	echo.
	call :COLOR_PRINT "Preparing virtual-env dir: %vritualEnvDirName% for the installation" "Yellow"
	set venvCmnd=python -m venv "%CD%\%vritualEnvDirName%" --system-site-packages
		:: Validate venv activation script
	if not exist "%CD%\%vritualEnvDirName%\Scripts\activate.bat" (
		echo Creating virtual-env dir: %CD%\%vritualEnvDirName%
		echo Executing: %venvCmnd%
		%venvCmnd%
		if !errorlevel! neq 0 echo. && call :COLOR_PRINT "Error - Bad exit code from creating virtual env command"  "RED" && echo Failure during execution of: %venvCmnd% && echo Failed to create a virtual env at: %CD%\%vritualEnvDirName% && echo. && echo Aborting.. && pause && exit /b 1
		echo Success - created virtual env at: %CD%\%vritualEnvDirName%
		if not exist "%CD%\%vritualEnvDirName%\Scripts\activate.bat" echo. && call :COLOR_PRINT "Error - Missing or unreacahble script  %CD%\%vritualEnvDirName%\Scripts\activate.bat"  "RED" && echo After creating a virtual env with exit code 0 at: %CD%\%vritualEnvDirName% && echo failed to locate venv activation script: %CD%\%vritualEnvDirName%\Scripts\activate.bat && echo Cannot activate the newly created virtual env && echo. && echo Aborting.. && pause && exit /b 1
	)
	
	
	:: Activate virtual env
	if not defined VIRTUAL_ENV (
		echo Variable 'VIRTUAL_ENV' is not defined - assuming virtual env is not activated yet
		echo Activating virtual environment now..
		echo Calling 'activate.bat' script: %CD%\%vritualEnvDirName%\Scripts\activate.bat
		call "%CD%\%vritualEnvDirName%\Scripts\activate.bat"
		if !errorlevel! neq 0 echo. && call :COLOR_PRINT "Error - Bad exit code from calling virtual env activation script  %CD%\%vritualEnvDirName%\Scripts\activate.bat"  "RED" && echo Attempted to activate newly created virtual env by calling activation script: %CD%\%vritualEnvDirName%\Scripts\activate.bat && echo  but calling activation script exited with a non zero code && echo Failed to activate the newly created virtual env: %CD%\%vritualEnvDirName% && echo. && echo Aborting.. && pause && exit /b 1
		if not defined VIRTUAL_ENV echo. && call :COLOR_PRINT "Error - Missing env VIRTUAL_ENV"  "RED" && echo Attempted to activate newly created virtual env by calling activation script: %CD%\%vritualEnvDirName%\Scripts\activate.bat && echo  but after calling the activation script, env: 'VIRTUAL_ENV' is stil missing && echo Failed to activate the newly created virtual env: %CD%\%vritualEnvDirName% && echo. && echo Aborting.. && pause && exit /b 1
		echo Success - Finished activating virtual environment
	)
	
	:: Remove already existing/installed package (if any..)
	echo Checking if package: %pkgName% is already installed..
	set installedPkgDir=%CD%\%vritualEnvDirName%\Lib\site-packages\%pkgName%
	pip freeze | findstr /i "%pkgName%" && call :COLOR_PRINT "Removing already installed package: %pkgName%" "Yellow" && echo Executing: pip uninstall %pkgName% -y && pip uninstall %pkgName% -y
	if exist "%installedPkgDir%" echo. && call :COLOR_PRINT "WARNING: Also removing installed package dir: %installedPkgDir%" "Yellow" && rmdir /q /s "%installedPkgDir%"
	if exist "%installedPkgDir%" rmdir /q /s "%installedPkgDir%"  && REM Sometimes need to execute rmdir twice [windows shit.. -_- ]
	if exist "%installedPkgDir%" echo. && call :COLOR_PRINT "WARNING: Failed to remove installed package dir: %installedPkgDir%" "Yellow" && echo. && echo Attempting to install anyway..
	
	
	echo.
	call :COLOR_PRINT "Installing pkg %pkgName%.." "Magenta"
	set installCmnd=python -m pip install --upgrade --no-deps --force-reinstall %CD%\dist\!wheelFile!
	echo. && echo Executing: %installCmnd% && echo.
	%installCmnd%
	if %errorlevel% neq 0 echo. && call :COLOR_PRINT "Error - Bad exit code from installing command"  "RED" && echo Failure during execution of: %installCmnd% && echo Failed to install pkg: '%pkgName%' from file: %CD%\dist\!wheelFile! && echo. && echo Aborting.. && pause && exit /b 1
	call :COLOR_PRINT "Success - Finished installing pkg: %pkgName%" "Green"
	echo Cleaning..
	if exist "src\%pkgName%.egg-info\*" echo Removing dir: "%CD%\src\%pkgName%.egg-info" && rmdir /q /s "src\%pkgName%.egg-info"
	if exist "src\%pkgName%.egg-info\*" rmdir /q /s "src\%pkgName%.egg-info"
	echo.


echo.
echo Done.
echo.
pause
endlocal
exit /b 0





:: Helper Functions

:COLOR_PRINT
set msg=%~1
set colored=%~2
if not defined colored set colored=WHITE
powershell -ExecutionPolicy ByPass -Command "Write-Host '%msg%' -ForegroundColor %colored%"
EXIT /B