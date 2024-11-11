from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_RESOLVED, CHAR_RESOLVED,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputProxyHostnameResolvedToIPAddress(oHTTPClient_unused, oProxyServerURL, sbIPAddress, sCanonicalName):
  sHost = fsCP437FromBytesString(oProxyServerURL.sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_RESOLVED,   CHAR_RESOLVED,
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
