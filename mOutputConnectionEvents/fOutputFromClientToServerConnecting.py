from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTING,
  COLOR_NORMAL,
  STR_CONNECTING_TO3,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerConnecting(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber):
  oConsole.fStatus(
    COLOR_ACTIVE,       "C",
    COLOR_CONNECTING,   STR_CONNECTING_TO3,
    COLOR_NORMAL,       "S",
    COLOR_NORMAL,       " Connecting to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,       "...",
  );