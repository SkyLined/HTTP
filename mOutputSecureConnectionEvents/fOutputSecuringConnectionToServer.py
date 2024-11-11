from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURING,
  COLOR_INFO,
  COLOR_NORMAL,
  STR_SECURING3,
);
oConsole = foConsoleLoader();

def fOutputSecuringConnectionToServer(oHTTPClient_unused, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   STR_SECURING3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Securing connection to server ",
    COLOR_INFO,       str(sbHost, "ascii", "strict"),
    COLOR_NORMAL,     "...",
  );