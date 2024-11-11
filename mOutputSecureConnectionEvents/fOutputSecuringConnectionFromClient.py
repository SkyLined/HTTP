from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_SECURING, STR_SECURING3,
);
oConsole = foConsoleLoader();

def fOutputSecuringConnectionFromClient(oHTTPClient_unused, oConnection, oSSLContext):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fStatus(
    COLOR_ACTIVE,       "S",
    COLOR_SECURING,     STR_SECURING3,
    COLOR_NORMAL,       "C",
    COLOR_NORMAL,       " Securing connection from client ",
    COLOR_INFO,         sRemoteIPAddress,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    COLOR_NORMAL,       "...",
  );