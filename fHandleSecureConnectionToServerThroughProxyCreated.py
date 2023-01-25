from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

def fHandleSecureConnectionToServerThroughProxyCreated(oClient, oConnection, oProxyServerURL, oServerURL):
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
