from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputServerHostInvalid(oHTTPClient_unused, *, sbHost):
  sHost = fsCP437FromBytesString(sbHost);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      3 * CHAR_ERROR,
    COLOR_ERROR,      "S",
    COLOR_NORMAL, " The server name or IP address ",
    COLOR_INFO, sHost,
    COLOR_NORMAL, " is not valid!",
  );
