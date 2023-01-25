from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputCannotConnectToHostname(oException, sbHostname, sCanonicalName, sIPAddress):
  sHostname = fsCP437FromBytesString(sbHostname);
  if sHostname.lower() != sIPAddress.lower():
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Cannot connect to hostname ",
      COLOR_INFO, sHostname,
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
      COLOR_NORMAL, ": ",
      COLOR_INFO, str(oException.sMessage),
      COLOR_NORMAL, ".",
    );
  elif not sCanonicalName.startswith("%s:" % sIPAddress):
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Cannot connect to IP address ",
      COLOR_HILITE, sIPAddress,
      COLOR_NORMAL, ": ",
      COLOR_INFO, str(oException.sMessage),
      COLOR_NORMAL, ".",
    );
