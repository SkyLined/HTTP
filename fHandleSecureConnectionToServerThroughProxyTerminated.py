from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

def fHandleSecureConnectionToServerThroughProxyTerminated(oClient, oConnection, oProxyServerURL, oServerURL):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, "×",
    COLOR_ACTIVE,       "P",
    COLOR_DISCONNECTED, "═",
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL, " Connection to server ",
    COLOR_INFO, str(oServerURL),
    COLOR_NORMAL, " through proxy ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, " terminated.",
  );
