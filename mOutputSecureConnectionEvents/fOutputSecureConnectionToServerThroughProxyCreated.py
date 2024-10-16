from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputSecureConnectionToServerThroughProxyCreated(oHTTPClient_unused, oConnection_unused, oProxyServerURL, oServerURL):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECTED,  "═",
    COLOR_ACTIVE,     "P",
    COLOR_CONNECTED,  "═",
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL, " Connected to server ",
    COLOR_INFO, str(oServerURL),
    COLOR_NORMAL, " through proxy ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, ".",
  );
