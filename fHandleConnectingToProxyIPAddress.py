from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleConnectingToProxyIPAddress(oHTTPClient, oProxyServerURL, sIPAddress, sbzHostname):
  sHostnameOrIPAddress = fsCP437FromBytesString(oProxyServerURL.sbHostname);
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
    ] if fbIsProvided(sbzHostname) else [],
    COLOR_NORMAL, "...",
  );