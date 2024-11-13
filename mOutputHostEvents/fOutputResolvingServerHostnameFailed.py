from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
  STR_RESOLVING_ERROR3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputResolvingServerHostnameFailed(oHTTPClient_unused, *, bHostname):
  sHostname = fsCP437FromBytesString(sbHostname);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR, STR_RESOLVING_ERROR3,
    COLOR_ERROR,      "S",
    COLOR_NORMAL,     " Cannot resolved server hostname ",
    COLOR_INFO,       sHostname,
    COLOR_NORMAL,     ".",
  );

