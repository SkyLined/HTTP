from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_HILITE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectingToServerIPAddressFailed(oHTTPClient_unused, oException, sbHost, sbIPAddress, uPortNumber):
  sHost = fsCP437FromBytesString(sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "-×→",
    COLOR_NORMAL,     "S",
    COLOR_NORMAL, " Connecting to server ",
    COLOR_INFO, ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uPortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
    ] if sbHost.lower() != sbIPAddress.lower() else [],
    COLOR_NORMAL, " failed!",
  );
  oConsole.fOutput(
    "    ",
    COLOR_INFO, CHAR_INFO, 
    COLOR_NORMAL, " ",
    COLOR_HILITE, str(oException.sMessage),
    COLOR_NORMAL, ".",
  );

