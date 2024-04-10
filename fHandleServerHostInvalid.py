from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleServerHostInvalid(oHTTPClient, sbHost):
  sHost = fsCP437FromBytesString(sbHost);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "·×·",
    COLOR_ERROR,      "S",
    COLOR_NORMAL, " The server name or IP address ",
    COLOR_INFO, sHost,
    COLOR_NORMAL, " is not valid!",
  );
