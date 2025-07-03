@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

REM Ran a standard tests file that executes HTTP with a number of arguments.
CALL "%~dp0\TestPythonApplication.cmd"
IF ERRORLEVEL 1 EXIT /B !ERRORLEVEL!

REM Test downloading a file 
CALL :fSetApplicationScript "%~dp0\.."
IF NOT EXIST "!sApplicationScript!" (
  ECHO - Cannot find application script [1;37m!sApplicationScript![0m.
  EXIT /B 1
);
SET sTempFilePath="!TEMP!\Test download for HTTP.txt"

CALL :RUN_TEST GET "https://ascii.skylined.nl" --download=!sTempFilePath!
IF ERRORLEVEL 1 EXIT /B !ERRORLEVEL!

IF NOT EXIST !sTempFilePath! (
  ECHO - Downloaded file !sTempFilePath! not found!
  EXIT /B 1
)
DEL !sTempFilePath! /Q

CALL :RUN_TEST GET "https://ascii.skylined.nl" --save=!sTempFilePath!
IF ERRORLEVEL 1 EXIT /B !ERRORLEVEL!

IF NOT EXIST !sTempFilePath! (
  ECHO - Saved response !sTempFilePath! not found!
  EXIT /B 1
)
DEL !sTempFilePath! /Q

ECHO + Test.cmd completed.
EXIT /B 0

:fSetApplicationScript
  SET sApplicationScript="%~dpn1\%~n1.cmd"
  EXIT /B 0

:RUN_TEST
  SET sArguments=%*
  CLS
  TITLE Testing !sApplicationScript! !sArguments!
  ECHO [1;37m!sApplicationScript! !sArguments![0m
  ECHO --------------------------------------------------------------------------------
  CALL !sApplicationScript! !sArguments!
  EXIT /B !ERRORLEVEL!
