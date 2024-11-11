from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, CHAR_DISCONNECTED,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputSecureConnectionToServerThroughProxyTerminated(oHTTPClient_unused, oConnection_unused, oProxyServerURL, oServerURL):
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_ACTIVE,       "P",
    COLOR_DISCONNECTED, CHAR_DISCONNECTED,
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL,       " Connection to server ",
    COLOR_INFO,         str(oServerURL),
    COLOR_NORMAL,       " through proxy ",
    COLOR_INFO,         str(oProxyServerURL),
    COLOR_NORMAL,       " terminated.",
  );
