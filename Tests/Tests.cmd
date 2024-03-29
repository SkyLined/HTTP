@ECHO OFF
SETLOCAL
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\HTTP Test stdout %RANDOM%.txt
SET TEST_DOWNLOAD_FILE_PATH=%TEMP%\HTTP Test download %RANDOM%.txt

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
CALL "%~dp0\..\HTTP.cmd" GET "http://example.com" -db >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test download GET http://skylined.nl (redirect to https://ascii.skylined.nl) with debug output...
CALL "%~dp0\..\HTTP.cmd" GET "http://skylined.nl" --debug -r=10 --download="%TEST_DOWNLOAD_FILE_PATH%" >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
IF NOT EXIST "%TEST_DOWNLOAD_FILE_PATH%" (
  ECHO - Downloaded file "%TEST_DOWNLOAD_FILE_PATH%" not found!
  IF EXIST "%REDIRECT_STDOUT_FILE_PATH%" (
    POWERSHELL $OutputEncoding = New-Object -Typename System.Text.UTF8Encoding; Get-Content -Encoding utf8 '"%REDIRECT_STDOUT_FILE_PATH%"'
  )
) ELSE (
  DEL "%TEST_DOWNLOAD_FILE_PATH%" /Q
)
IF EXIST "%REDIRECT_STDOUT_FILE_PATH%" (
  DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q
)
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
