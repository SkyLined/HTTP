@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
SET sScript="%~dpn0.py"
SET sArguments=%*

IF DEFINED PYTHON (
  IF EXIST !PYTHON! GOTO :RUN_PYTHON
)
IF DEFINED PYTHONPATH (
  SET PYTHON=!PYTHONPATH!\python.exe
  IF EXIST !PYTHON! GOTO :RUN_PYTHON
)
REM Try to detect the location of python automatically
FOR /F "usebackq delims=" %%I IN (`where "python" 2^>nul`) DO (
  SET PYTHON="%%~fI"
  IF EXIST !PYTHON! GOTO :RUN_PYTHON
)
REM Check if python is found in its default installation path.
FOR /D %%I IN ("!LOCALAPPDATA!\Programs\Python\*") DO (
  SET PYTHON="%%~fI\python.exe"
  IF EXIST !PYTHON! GOTO :RUN_PYTHON
)
ECHO - Cannot find python.exe, please set the "PYTHON" environment variable to the
ECHO   correct path, or add Python to the "PATH" environment variable.
EXIT /B 1

:RUN_PYTHON
  REM We did not find `/?` in the arguments.
  ECHO !PYTHON! !sScript! !sArguments!
  CALL !PYTHON! !sScript! !sArguments!
  EXIT /B !ERRORLEVEL!
