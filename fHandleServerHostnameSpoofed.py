from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleServerHostnameSpoofed(oHTTPClient, sbHostname, sbSpoofedHostname):
  sHostname = fsCP437FromBytesString(sbHostname);
  sSpoofedHostname = fsCP437FromBytesString(sbSpoofedHostname);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_WARNING,    "··»",
    COLOR_WARNING,    "S",
    COLOR_NORMAL, " The server name or IP address ",
    COLOR_INFO, sHostname,
    COLOR_NORMAL, " has been spoofed as ",
    COLOR_INFO, sSpoofedHostname,
    COLOR_NORMAL, ".",
  );
