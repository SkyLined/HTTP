from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

def fHandleProxyHostnameOrIPAddressInvalid(oHTTPClient, oProxyServerURL):
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
