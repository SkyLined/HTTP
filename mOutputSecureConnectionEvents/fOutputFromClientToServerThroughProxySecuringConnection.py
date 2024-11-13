from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_SECURING, CHAR_SECURING,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerThroughProxySecuringConnection(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber, oSSLContext):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_ACTIVE,     "P",
    COLOR_SECURING,   CHAR_SECURING,
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL,     " Securing connection to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,     " through proxy ",
    fasOutputAddress(sbHost = oProxyServerURL.sbHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oProxyServerURL.uPortNumber),
    COLOR_NORMAL,     ".",
  );
