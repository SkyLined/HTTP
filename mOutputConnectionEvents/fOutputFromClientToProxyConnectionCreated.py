from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, CHAR_CONNECTED_TO,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToProxyConnectionCreated(oHTTPClient_unused, *, oProxyServerURL, sbIPAddress, uPortNumber, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  CHAR_CONNECTED_TO,
    COLOR_ACTIVE,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connected to proxy ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,     ".",
  );
