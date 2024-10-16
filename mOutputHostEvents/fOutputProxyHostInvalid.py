from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputProxyHostInvalid(oHTTPClient_unused, oProxyServerURL):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "×",
    COLOR_ERROR,      "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL, " The proxy name or IP address ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, " is not valid!",
  );
