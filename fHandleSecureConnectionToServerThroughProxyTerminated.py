from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleSecureConnectionToServerThroughProxyTerminated(oClient, oConnection, oProxyServerURL, oServerURL):
  sHostnameOrIPAddress = fsCP437FromBytesString(sbHostnameOrIPAddress);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,       "C",
    COLOR_DISCONNECTED, "×",
    COLOR_ACTIVE,       "P",
    COLOR_DISCONNECTED, "═",
    COLOR_INACTIVE,     "S",
    COLOR_NORMAL, " Connection to server ",
    COLOR_INFO, str(oServerURL),
    COLOR_NORMAL, " through proxy ",
    COLOR_INFO, str(oProxyServerURL),
    COLOR_NORMAL, " terminated.",
  );
