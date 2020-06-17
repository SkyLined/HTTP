@ECHO OFF
SETLOCAL
SET TEST_DOWNLOAD_FILE_PATH=%TEMP%\HTTP Test file %RANDOM%.txt

ECHO   * Test version check...
CALL "%~dp0HTTP.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test help...
CALL "%~dp0HTTP.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test GET http://example.com...
CALL "%~dp0HTTP.cmd" GET "http://example.com" -db
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test GET http://example.com...
CALL "%~dp0HTTP.cmd" GET "http://example.com" --download="%TEST_DOWNLOAD_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test GET https://example.com...
CALL "%~dp0HTTP.cmd" GET "https://example.com" --download="%TEST_DOWNLOAD_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

DEL "%TEST_DOWNLOAD_FILE_PATH%" /Q

ECHO + Done.
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  IF EXIST "%TEST_DOWNLOAD_FILE_PATH%" DEL "%TEST_DOWNLOAD_FILE_PATH%" /Q
  ENDLOCAL
  EXIT /B 1
