from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  CHAR_RESOLVING_ERROR,
);
oConsole = foConsoleLoader();

def fOutputResolvingProxyHostnameFailed(oHTTPClient_unused, *, sbHostname, oException):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_RESOLVING_ERROR,
    COLOR_ERROR,      "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Cannot resolved proxy hostname ",
    COLOR_INFO,       str(sbHostname),
    COLOR_NORMAL,     ".",
  );

