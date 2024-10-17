from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECT,
  COLOR_NORMAL,
  COLOR_INFO,
);
oConsole = foConsoleLoader();

def fOutputConnectionFromClientCreated(oHTTPServer_unused, oConnection):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_CONNECT,      "←--",
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL,       " Connection from client: ",
    COLOR_INFO,         sRemoteIPAddress,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    COLOR_NORMAL,       " created.",
  );
