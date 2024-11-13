from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_NORMAL,
  COLOR_SECURING, STR_SECURING3,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputToServerFromClientSecuringConnection(oHTTPClient_unused, *, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,       "S",
    COLOR_SECURING,     STR_SECURING3,
    COLOR_NORMAL,       "C",
    COLOR_NORMAL,       " Securing connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,       "...",
  );