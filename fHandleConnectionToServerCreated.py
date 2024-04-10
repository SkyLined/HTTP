from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;
oConsole = foConsoleLoader();

def fHandleConnectionToServerCreated(oClient, oConnection, sbHost):
  sHost = fsCP437FromBytesString(sbHost);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_CONNECT,    "--→",
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL, " Connected to server ",
    COLOR_INFO, ("[%s]" if ":" in sHost else "%s") % sHost,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uRemotePortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sRemoteIPAddress,
    ] if sHost.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL, ".",
  );
