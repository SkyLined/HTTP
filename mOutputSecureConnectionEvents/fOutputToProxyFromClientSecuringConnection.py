from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INACTIVE,
  COLOR_NORMAL,
  COLOR_SECURING, CHAR_SECURING,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputToProxyFromClientSecuringConnection(oHTTPClient_unused, *, oConnection, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,     "...",
  );