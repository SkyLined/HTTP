from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_OK, CHAR_OK,
  COLOR_HILITE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputHostResolved(oHTTPClient_unused, *, sbHost, sCanonicalName, sbIPAddress):
  sHost = fsCP437FromBytesString(sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  if sHost.lower() != sIPAddress.lower():
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Resolved hostname ",
      COLOR_INFO, sHost,
      COLOR_NORMAL, " as IP address ",
      COLOR_INFO, sIPAddress,
      COLOR_NORMAL, 
      [
        " (",
        COLOR_INFO, sCanonicalName,
        COLOR_NORMAL, ")",
      ] if sCanonicalName and sCanonicalName.lower() != sHost.lower() else [],
      ".",
    );
  elif not sCanonicalName.startswith("%s:" % sIPAddress):
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Resolved IP address ",
      COLOR_HILITE, sIPAddress,
      COLOR_NORMAL, " as hostname ",
      COLOR_INFO, sCanonicalName,
      COLOR_NORMAL, ".",
    );
