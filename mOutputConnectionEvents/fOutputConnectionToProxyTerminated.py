from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_DISCONNECTED,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputConnectionToProxyTerminated(oHTTPClient_unused, oConnection, oProxyServerURL):
  sHost = fsCP437FromBytesString(oProxyServerURL.sbHost);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, "×",
    COLOR_ACTIVE,       "P",
    COLOR_NORMAL,       " ",
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL, " Connection to proxy ",
    COLOR_INFO, str(oProxyServerURL),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sRemoteIPAddress,
    ] if sHost.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL, " terminated.",
  );
