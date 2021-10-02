@echo off

:: This script compiles the python pkg


set pkgName=davis8988-hello
set repoDir=%~dp0..\..
set setupFile=%repoDir%\setup.py

echo Compiling pkg: '%pkgName%'

echo Validating env..
if not exist "%setupFile%" echo. && echo Error - Missing or unreacahble setup.py file at: "%setupFile%" && echo Cannot compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1
echo CD into repo root dir: %repoDir%
pushd "%repoDir%"
if %errorlevel% neq 0 echo. && echo Error - Failed to CD into "%repoDir%" && echo. && echo Aborting.. && pause && exit /b 1
echo OK
echo.

powershell -ExecutionPolicy ByPass -Command "Write-Host 'Compiling..' -ForegroundColor Yellow; echo ''"

set compileCmnd=python "%setupFile%" bdist_wheel
echo Executing: %compileCmnd%
%compileCmnd%
if %errorlevel% neq 0 echo. && echo Error - Bad exit code && echo Failure during execution of: %compileCmnd% && echo Failed to compile pkg: '%pkgName%' && echo. && echo Aborting.. && pause && exit /b 1

powershell -ExecutionPolicy ByPass -Command "Write-Host 'Success' -ForegroundColor Green"

echo.
echo Done.
echo.
pause


