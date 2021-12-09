from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fHandleResolvingProxyHostname(oHTTPClient, oProxyServerURL):
  oConsole.fStatus(
    COLOR_ACTIVE,   "C",
    COLOR_CONNECT,  "··»",
    COLOR_NORMAL,   "S",
    COLOR_NORMAL, " Resolving proxy hostname ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, "...",
  );
