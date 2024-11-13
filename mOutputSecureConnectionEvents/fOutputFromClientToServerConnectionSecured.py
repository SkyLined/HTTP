from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, STR_SECURED3,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerConnectionSecured(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_SECURED,    STR_SECURED3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Secured connection to server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     ".",
  );