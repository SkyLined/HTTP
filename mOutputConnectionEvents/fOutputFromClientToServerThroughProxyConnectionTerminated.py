from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, CHAR_DISCONNECTED,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;
from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToServerThroughProxyConnectionTerminated(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_INACTIVE,     "P",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL,       " Connection to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,       " through proxy ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " terminated.",
  );