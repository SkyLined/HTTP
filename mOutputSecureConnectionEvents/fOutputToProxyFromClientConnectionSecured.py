from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, CHAR_SECURED,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputToProxyFromClientConnectionSecured(oHTTPClient_unused, *, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_SECURED,    CHAR_SECURED,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Secured connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,     ".",
  );