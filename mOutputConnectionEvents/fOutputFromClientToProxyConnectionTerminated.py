from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, CHAR_DISCONNECTED,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToProxyConnectionTerminated(oHTTPClient_unused, *, oConnection, oProxyServerURL, sbIPAddress, uPortNumber):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_ACTIVE,       "P",
    COLOR_NORMAL,       " ",
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL,       " Connection to proxy ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " terminated.",
  );
