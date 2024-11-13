from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, CHAR_CONNECTED_TO,
  COLOR_CONNECTING, CHAR_CONNECTING_TO,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;
from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToServerThroughProxyConnecting(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  CHAR_CONNECTED_TO,
    COLOR_ACTIVE,     "P",
    COLOR_CONNECTING, CHAR_CONNECTING_TO,
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,     " through proxy ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,     "...",
  );