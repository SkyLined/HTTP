from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTING, CHAR_CONNECTING_TO,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectingToProxyIPAddress(oHTTPClient_unused, oProxyServerURL, sbIPAddress):
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTING, CHAR_CONNECTING_TO,
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to proxy ",
    COLOR_INFO,       str(oProxyServerURL),
    [
      COLOR_NORMAL,   " using IP address ",
      COLOR_INFO,     sIPAddress,
    ] if oProxyServerURL.sbHost.lower() != sbIPAddress.lower() else [],
    COLOR_NORMAL,     "...",
  );