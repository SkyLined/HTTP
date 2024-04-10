from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mNotProvided import fbIsProvided;
oConsole = foConsoleLoader();

def fHandleConnectingToProxyIPAddress(oHTTPClient, oProxyServerURL, sbIPAddress):
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "→",
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL, " Connecting to proxy ",
    COLOR_INFO, str(oProxyServerURL),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
    ] if oProxyServerURL.sbHost.lower() != sbIPAddress.lower() else [],
    COLOR_NORMAL, "...",
  );