from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, STR_SECURED3,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputConnectionToServerSecured(oHTTPClient_unused, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_SECURED,    STR_SECURED3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Secured connection to server ",
    COLOR_INFO,       str(sbHost, "ascii", "strict"),
    COLOR_NORMAL,     ".",
  );