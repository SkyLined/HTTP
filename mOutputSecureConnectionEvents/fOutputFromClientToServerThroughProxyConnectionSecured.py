from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURED, CHAR_SECURED,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerThroughProxyConnectionSecured(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_SECURED,    CHAR_SECURED,
    COLOR_ACTIVE,     "P",
    COLOR_SECURED,    CHAR_SECURED,
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL,     " Secured connection to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,     " through proxy ",
    fasOutputAddress(sbHost = oProxyServerURL.sbHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oProxyServerURL.uPortNumber),
    COLOR_NORMAL,     ".",
  );
