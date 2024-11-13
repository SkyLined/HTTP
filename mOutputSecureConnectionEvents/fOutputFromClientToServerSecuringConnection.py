from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURING, CHAR_SECURING,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerSecuringConnection(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_NORMAL,     "P",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL,     " Securing connection to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     "...",
  );