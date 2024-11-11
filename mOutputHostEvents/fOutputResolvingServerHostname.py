from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_RESOLVING, STR_RESOLVING3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputResolvingServerHostname(oHTTPClient_unused, sbHostname):
  sHostname = fsCP437FromBytesString(sbHostname);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_RESOLVING,  STR_RESOLVING3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Resolving server hostname ",
    COLOR_INFO,       sHostname,
    COLOR_NORMAL,     "...",
  );
