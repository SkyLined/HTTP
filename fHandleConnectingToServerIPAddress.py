from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import fbIsProvided;
oConsole = foConsoleLoader();

def fHandleConnectingToServerIPAddress(oHTTPClient, sbHost, sbIPAddress, uPortNumber):
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