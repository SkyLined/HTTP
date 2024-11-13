from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, STR_CONNECTED_TO3,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToServerConnectionCreated(oHTTPServer_unused, *, sbHost, uPortNumber, sbIPAddress, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_CONNECTED,    STR_CONNECTED_TO3,
    COLOR_ACTIVE,       "S",
    COLOR_NORMAL,       " Connection to server ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " created.",
  );
