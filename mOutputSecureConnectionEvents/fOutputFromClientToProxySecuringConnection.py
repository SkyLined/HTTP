from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INACTIVE,
  COLOR_NORMAL,
  COLOR_SECURING, CHAR_SECURING,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToProxySecuringConnection(oHTTPClient_unused, *, oProxyServerURL, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection to the proxy server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     "...",
  );