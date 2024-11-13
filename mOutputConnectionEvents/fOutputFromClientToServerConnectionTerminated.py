from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, STR_DISCONNECTED3,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputFromClientToServerConnectionTerminated(oHTTPServer_unused, *, sbHost, sbIPAddress, uPortNumber, oConnection):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, STR_DISCONNECTED3,
    COLOR_ACTIVE,       "S",
    COLOR_NORMAL,       " Connection to server ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " terminated.",
  );
