from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_HILITE,
  COLOR_INACTIVE,
  COLOR_INFO, CHAR_INFO,
  COLOR_NORMAL,
  CHAR_CONNECTING_TO_ERROR,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromProxyToServerConnectingFailed(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber, oException):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_NORMAL,     " ",
    COLOR_ACTIVE,     "P",
    COLOR_ERROR,      CHAR_CONNECTING_TO_ERROR,
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     " failed.",
  );
  oConsole.fOutput(
    "    ",
    COLOR_INFO, CHAR_INFO, 
    COLOR_NORMAL, " ",
    COLOR_HILITE, str(oException.sMessage),
    COLOR_NORMAL, ".",
  );

