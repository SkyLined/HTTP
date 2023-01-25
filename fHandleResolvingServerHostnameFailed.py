from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleResolvingServerHostnameFailed(oHTTPClient, sbHostname):
  sHostname = fsCP437FromBytesString(sbHostname);
  oConsole.fOutput(
    COLOR_ACTIVE,   "C",
    COLOR_ERROR,    "·×·",
    COLOR_ERROR,    "S",
    COLOR_NORMAL, " Cannot resolved server hostname ",
    COLOR_INFO, sHostname,
    COLOR_NORMAL, ".",
  );

