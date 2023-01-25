from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleResolvingProxyHostnameFailed(oHTTPClient, oProxyServerURL):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "×",
    COLOR_ERROR,      "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL, " Cannot resolved proxy hostname ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, ".",
  );

