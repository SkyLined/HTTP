from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_HILITE,
  COLOR_INFO, CHAR_INFO,
  COLOR_NORMAL,
  STR_CONNECTING_TO_ERROR3,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerConnectingFailed(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber, oException):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      STR_CONNECTING_TO_ERROR3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Connecting to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     " failed!",
  );
  oConsole.fOutput(
    "    ",
    COLOR_INFO,       CHAR_INFO, 
    COLOR_NORMAL,     " ",
    COLOR_HILITE,     str(oException.sMessage),
    COLOR_NORMAL,     ".",
  );

