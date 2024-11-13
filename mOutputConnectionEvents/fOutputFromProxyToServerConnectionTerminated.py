from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, CHAR_DISCONNECTED,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromProxyToServerConnectionTerminated(oHTTPClient_unused, *, sbHost, sbIPAddress, uPortNumber, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL,       " ",
    COLOR_ACTIVE,       "P",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL,       " Connected to server ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " terminated.",
  );
