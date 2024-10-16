from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_HILITE,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectingToProxyIPAddressFailed(oHTTPClient_unused, oException, oProxyServerURL, sbIPAddress):
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "×",
    COLOR_ERROR,      "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL, " Connecting to proxy ",
    COLOR_INFO, str(oProxyServerURL),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
    ] if oProxyServerURL.sbHost.lower() != sbIPAddress.lower() else [],
    COLOR_NORMAL, " failed!",
  );
  oConsole.fOutput(
    "    ",
    COLOR_INFO, CHAR_INFO, 
    COLOR_NORMAL, " ",
    COLOR_HILITE, str(oException.sMessage),
    COLOR_NORMAL, ".",
  );

