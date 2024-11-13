from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTING, CHAR_CONNECTING_TO,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromProxyToServerConnecting(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_NORMAL,     " ",
    COLOR_ACTIVE,     "P",
    COLOR_CONNECTING, CHAR_CONNECTING_TO,
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     "...",
  );