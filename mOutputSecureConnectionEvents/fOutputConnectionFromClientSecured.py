from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, STR_SECURED3,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputConnectionFromClientSecured(oHTTPClient_unused, oConnection, oSSLContext):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fOutput(
    COLOR_ACTIVE,     "S",
    COLOR_SECURED,    STR_SECURED3,
    COLOR_INACTIVE,   "C",
    COLOR_NORMAL,     " Secured connection from client ",
    COLOR_INFO,       sRemoteIPAddress,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    COLOR_NORMAL,     ".",
  );