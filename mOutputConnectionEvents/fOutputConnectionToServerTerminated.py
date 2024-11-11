from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED, STR_DISCONNECTED3,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectionToServerTerminated(oHTTPClient_unused, oConnection, sbHost):
  sHost = fsCP437FromBytesString(sbHost);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, STR_DISCONNECTED3,
    COLOR_ACTIVE,       "S",
    COLOR_NORMAL,       " Connection to server ",
    COLOR_INFO,         ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    [
      COLOR_NORMAL,     " using IP address ",
      COLOR_INFO,       sRemoteIPAddress,
    ] if sHost.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL,       " terminated.",
  );
