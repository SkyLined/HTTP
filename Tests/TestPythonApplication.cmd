@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

REM This script lives in the Tests folder. The name of its parent folder should
REM be the same as the name of the product as well as the name of the main
REM script to run the application. Let's save that name in a variable:
CALL :fSetApplicationScript "%~dp0\.."
IF NOT EXIST "!sApplicationScript!" (
  ECHO - Cannot find application script [1;37m!sApplicationScript![0m.
  EXIT /B 1
);

REM There should be a "Test Application Arguments.txt" file in the Tests folder
REM that contains a set of arguments to test on each one of its lines.
REM lets read those lines and run the application script with them:
IF NOT EXIST "%~dp0\Test Application Arguments.txt" (
  ECHO - Cannot find argument list file [1;37m%~dp0\Test Application Arguments.txt[0m.
  EXIT /B 1
);


FOR /F "usebackq tokens=*" %%A in ("%~dp0\Test Application Arguments.txt") DO (
  SET sArguments=%%A
  REM Skip comment lines that start with "#"
  IF NOT "!sArguments:~0,1!" == "#" (
    CLS
    TITLE Testing !sApplicationScript! !sArguments!
    ECHO [1;37m!sApplicationScript! !sArguments![0m
    ECHO --------------------------------------------------------------------------------
    CALL !sApplicationScript! !sArguments!
    IF ERRORLEVEL 1 EXIT /B !ERRORLEVEL!
  )
)
TITLE Testing completed.
EXIT /B 0

:fSetApplicationScript
  SET sApplicationScript="%~dpn1\%~n1.cmd"
  EXIT /B 0