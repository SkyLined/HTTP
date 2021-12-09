@ECHO OFF
SETLOCAL
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\BugId Test stdout %RANDOM%.txt
SET TEST_DOWNLOAD_FILE_PATH=%TEMP%\HTTP Test file %RANDOM%.txt

ECHO   * Test usage help...
CALL "%~dp0\..\HTTP.cmd" --help >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version info...
CALL "%~dp0\..\HTTP.cmd" --version >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version check...
CALL "%~dp0\..\HTTP.cmd" --version-check >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license info...
CALL "%~dp0\..\HTTP.cmd" --license >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license update...
CALL "%~dp0\..\HTTP.cmd" --license-update >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test GET http://example.com...
CALL "%~dp0\..\HTTP.cmd" GET "http://example.com" -db
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test GET http://duckduckgo.com (redirect to https) with debug output...
CALL "%~dp0\..\HTTP.cmd" GET "http://example.com" --debug -r=1
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test download GET http://example.com...
CALL "%~dp0\..\HTTP.cmd" GET "http://example.com" --download="%TEST_DOWNLOAD_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test download GET https://example.com...
CALL "%~dp0\..\HTTP.cmd" GET "https://example.com" --download="%TEST_DOWNLOAD_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

DEL "%TEST_DOWNLOAD_FILE_PATH%" /Q
DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q

ECHO + Test.cmd completed.
ENDLOCAL
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  CALL :CLEANUP
  ENDLOCAL
  EXIT /B 3

:CLEANUP
  IF EXIST "%TEST_DOWNLOAD_FILE_PATH%" (
    DEL "%TEST_DOWNLOAD_FILE_PATH%" /Q
  )
  IF EXIST "%REDIRECT_STDOUT_FILE_PATH%" (
    POWERSHELL $OutputEncoding = New-Object -Typename System.Text.UTF8Encoding; Get-Content -Encoding utf8 '"%REDIRECT_STDOUT_FILE_PATH%"'
    DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q
  )
