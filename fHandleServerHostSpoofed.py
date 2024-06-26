﻿from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleServerHostSpoofed(oHTTPClient, sbHost, sbSpoofedHost):
  sHost = fsCP437FromBytesString(sbHost);
  sSpoofedHost = fsCP437FromBytesString(sbSpoofedHost);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_WARNING,    "··»",
    COLOR_WARNING,    "S",
    COLOR_NORMAL, " The server name or IP address ",
    COLOR_INFO, sHost,
    COLOR_NORMAL, " has been spoofed as ",
    COLOR_INFO, sSpoofedHost,
    COLOR_NORMAL, ".",
  );
