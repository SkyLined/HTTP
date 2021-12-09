from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleConnectingToServerIPAddress(oHTTPClient, sbHostnameOrIPAddress, sIPAddress, uPortNumber, sbzHostname):
  sHostnameOrIPAddress = fsCP437FromBytesString(sbHostnameOrIPAddress);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "--→",
    COLOR_NORMAL,     "S",
    COLOR_NORMAL, " Connecting to server ",
    COLOR_INFO, ("[%s]" if ":" in sHostnameOrIPAddress else "%s") % sHostnameOrIPAddress,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uPortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
    ] if fbIsProvided(sbzHostname) else [],
    COLOR_NORMAL, "...",
  );