from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleProxyHostnameResolvedToIPAddress(oHTTPClient, oProxyServerURL, sbIPAddress, sCanonicalName):
  sHost = fsCP437FromBytesString(oProxyServerURL.sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "»",
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL, " Resolved proxy hostname ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, " as IP address ",
    COLOR_INFO, sIPAddress,
    COLOR_NORMAL, 
    [
      " (",
      COLOR_INFO, sCanonicalName,
      COLOR_NORMAL, ")",
    ] if sCanonicalName and sCanonicalName.lower() != sHost.lower() else [],
    ".",
  );
