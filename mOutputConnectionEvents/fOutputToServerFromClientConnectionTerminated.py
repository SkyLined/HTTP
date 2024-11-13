from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, STR_DISCONNECTED3,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputToServerFromClientConnectionTerminated(oHTTPServer_unused, *, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_DISCONNECTED, STR_DISCONNECTED3,
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL,       " Connection from client: ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " terminated.",
  );
