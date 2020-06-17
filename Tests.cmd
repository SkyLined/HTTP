@ECHO OFF
SETLOCAL
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\zyp Test stdout %RANDOM%.txt
SET TEST_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.txt
SET TEST_ZIP_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.zip

ECHO   * Test version check...
CALL "%~dp0zyp.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0unzyp.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test help...
CALL "%~dp0zyp.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0unzyp.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Zipping test file...
ECHO Hello, world! >"%TEST_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0zyp.cmd" "%TEST_FILE_PATH%" "%TEST_ZIP_FILE_PATH%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
DEL "%TEST_FILE_PATH%" /Q

ECHO   * Listing zipped test file...
CALL "%~dp0unzyp.cmd" --list "%TEST_ZIP_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Unzipping test file...
CALL "%~dp0unzyp.cmd" "%TEST_ZIP_FILE_PATH%" "%TEMP%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
IF NOT EXIST "%TEST_FILE_PATH%" (
  ECHO Unzipping did not re-create test file!
  DEL %TEST_ZIP_FILE_PATH% /Q
  EXIT /B 1
)
DEL "%TEST_FILE_PATH%" /Q
DEL "%TEST_ZIP_FILE_PATH%" /Q

ECHO + Done.
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  IF EXIST "%TEST_FILE_PATH%" DEL "%TEST_FILE_PATH%" /Q
  IF EXIST "%TEST_ZIP_FILE_PATH%" DEL "%TEST_ZIP_FILE_PATH%" /Q
  ENDLOCAL
  EXIT /B 1
