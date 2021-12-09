from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fHandleProxyHostnameResolvedToIPAddress(oHTTPClient, oProxyServerURL, sIPAddress, sCanonicalName):
  sHostnameOrIPAddress = fsCP437FromBytesString(oProxyServerURL.sbHostname);
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
    ] if sCanonicalName and sCanonicalName.lower() != sHostnameOrIPAddress.lower() else [],
    ".",
  );
