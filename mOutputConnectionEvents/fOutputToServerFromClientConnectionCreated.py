from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, STR_CONNECTED_FROM3,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputToServerFromClientConnectionCreated(oHTTPServer_unused, *, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_CONNECTED,    STR_CONNECTED_FROM3,
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL,       " Connection from client: ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " created.",
  );
