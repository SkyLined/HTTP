from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, STR_CONNECTED_TO3,
  COLOR_ACTIVE,
  COLOR_NORMAL,
  COLOR_INFO,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectionToServerCreated(oHTTPClient_unused, sbHost, uPortNumber, sbIPAddress, oConnection):
  sHost = fsCP437FromBytesString(sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  STR_CONNECTED_TO3,
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL,     " Connected to server ",
    COLOR_INFO,       ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL,     ":",
    COLOR_INFO,       str(uPortNumber),
    [
      COLOR_NORMAL,   " using IP address ",
      COLOR_INFO,     sIPAddress,
    ] if sHost.lower() != sIPAddress.lower() else [],
    COLOR_NORMAL,     ".",
  );
