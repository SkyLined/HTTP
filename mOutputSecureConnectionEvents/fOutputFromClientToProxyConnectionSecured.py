from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, CHAR_SECURED,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToProxyConnectionSecured(oHTTPClient_unused, *, oProxyServerURL, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_SECURED,    CHAR_SECURED,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Secured connection to proxy server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     ".",
  );