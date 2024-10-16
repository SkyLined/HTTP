from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECT,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectingToServerIPAddress(oHTTPClient_unused, sbHost, sbIPAddress, uPortNumber):
  sHost = fsCP437FromBytesString(sbHost);
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fStatus(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "--→",
    COLOR_NORMAL,     "S",
    COLOR_NORMAL, " Connecting to server ",
    COLOR_INFO, ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uPortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
    ] if sbHost.lower() != sbIPAddress.lower() else [],
    COLOR_NORMAL, "...",
  );