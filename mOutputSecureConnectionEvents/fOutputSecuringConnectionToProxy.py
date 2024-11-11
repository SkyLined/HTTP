from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_INACTIVE,
  COLOR_NORMAL,
  COLOR_SECURING, CHAR_SECURING,
);
oConsole = foConsoleLoader();

def fOutputSecuringConnectionToProxy(oHTTPClient_unused, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection to the proxy server ",
    COLOR_INFO,       str(sbHost, "ascii", "strict"),
    COLOR_NORMAL,     "...",
  );