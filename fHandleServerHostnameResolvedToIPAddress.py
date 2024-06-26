﻿from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fHandleServerHostnameResolvedToIPAddress(oHTTPClient, sbHostname, sbIPAddress, sCanonicalName):
  sHostname = fsCP437FromBytesString(sbHostname);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "··»",
    COLOR_NORMAL,     "S",
    COLOR_NORMAL, " Resolved hostname ",
    COLOR_INFO, sHostname,
    COLOR_NORMAL, " as IP address ",
    COLOR_INFO, sIPAddress,
    COLOR_NORMAL, 
    [
      " (",
      COLOR_INFO, sCanonicalName,
      COLOR_NORMAL, ")",
    ] if sCanonicalName and sCanonicalName.lower() != sHostname.lower() else [],
    ".",
  );
