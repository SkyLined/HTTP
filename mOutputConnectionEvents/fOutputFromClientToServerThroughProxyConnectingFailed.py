from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, CHAR_CONNECTED_TO,
  COLOR_ERROR, CHAR_CONNECTING_TO_ERROR,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;
from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToServerThroughProxyConnectingFailed(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber, uStatusCode):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  CHAR_CONNECTED_TO,
    COLOR_ACTIVE,     "P",
    COLOR_ERROR,      CHAR_CONNECTING_TO_ERROR,
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,     " through proxy ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,     " failed with status code ",
    COLOR_INFO,       str(uStatusCode),
    COLOR_NORMAL,     ".",
  );