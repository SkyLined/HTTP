from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleResolvingServerHostname(oHTTPClient, sbHostname):
  sHostname = fsCP437FromBytesString(sbHostname);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "··»",
    COLOR_NORMAL,     "S",
    COLOR_NORMAL, " Resolving server hostname ",
    COLOR_INFO, sHostname,
    COLOR_NORMAL, "...",
  );
