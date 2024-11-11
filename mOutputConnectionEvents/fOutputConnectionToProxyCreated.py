from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, CHAR_CONNECTED_TO,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectionToProxyCreated(oHTTPClient_unused, oProxyServerURL, sbIPAddress, uPortNumber, oConnection):
  sHost = fsCP437FromBytesString(oProxyServerURL.sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  CHAR_CONNECTED_TO,
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connected to proxy ",
    COLOR_INFO,       str(oProxyServerURL),
    [
      COLOR_NORMAL,   " using IP address ",
      COLOR_INFO,     sIPAddress,
    ] if sHost.lower() != sIPAddress.lower() else [],
    COLOR_NORMAL,     ".",
  );
