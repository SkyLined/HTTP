from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTING, CHAR_CONNECTING_TO,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToProxyConnecting(oHTTPClient_unused, *, oProxyServerURL, sbIPAddress, uPortNumber):
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTING, CHAR_CONNECTING_TO,
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to proxy ",
    fasOutputAddress(sbHost = oProxyServerURL.sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     "...",
  );