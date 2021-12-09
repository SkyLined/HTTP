from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleConnectionToProxyTerminated(oClient, oConnection, oProxyServerURL):
  sHostnameOrIPAddress = fsCP437FromBytesString(oProxyServerURL.sbHostname);
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
    ] if sHostnameOrIPAddress.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL, " terminated.",
  );
