from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_RESOLVING, STR_RESOLVING3,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

def fOutputResolvingProxyHostname(oHTTPClient_unused, *, oProxyServerURL):
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_RESOLVING,  STR_RESOLVING3,
    COLOR_NORMAL,     "S",
    COLOR_NORMAL,     " Resolving proxy hostname ",
    COLOR_INFO,       str(oProxyServerURL),
    COLOR_NORMAL,     "...",
  );
