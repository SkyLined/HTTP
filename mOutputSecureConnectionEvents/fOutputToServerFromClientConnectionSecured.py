from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, STR_SECURED3,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputToServerFromClientConnectionSecured(oHTTPClient_unused, *, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "S",
    COLOR_SECURED,    STR_SECURED3,
    COLOR_INACTIVE,   "C",
    COLOR_NORMAL,     " Secured connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,     ".",
  );