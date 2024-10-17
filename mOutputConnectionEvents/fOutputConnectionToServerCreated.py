from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECT,
  COLOR_ACTIVE,
  COLOR_NORMAL,
  COLOR_INFO,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectionToServerCreated(oHTTPClient_unused, oConnection, sbHost):
  sHost = fsCP437FromBytesString(sbHost);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "--→",
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL, " Connected to server ",
    COLOR_INFO, ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL, ": ",
    COLOR_INFO, str(uRemotePortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sRemoteIPAddress,
    ] if sHost.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL, ".",
  );
