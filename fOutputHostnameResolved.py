from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputHostnameResolved(sbHostname, sCanonicalName, sbIPAddress):
  sHostname = fsCP437FromBytesString(sbHostname);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  if sHostname.lower() != sIPAddress.lower():
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
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
  elif not sCanonicalName.startswith("%s:" % sIPAddress):
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Resolved IP address ",
      COLOR_HILITE, sIPAddress,
      COLOR_NORMAL, " as hostname ",
      COLOR_INFO, sCanonicalName,
      COLOR_NORMAL, ".",
    );
