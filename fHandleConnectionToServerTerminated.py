from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleConnectionToServerTerminated(oClient, oConnection, sbHostnameOrIPAddress):
  # We only show this message if the user provided a hostname instead of an IP address.
  sHostnameOrIPAddress = fsCP437FromBytesString(sbHostnameOrIPAddress);
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_DISCONNECT, "-×→",
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL, " Connection to server ",
    COLOR_INFO, ("[%s]" if ":" in sHostnameOrIPAddress else "%s") % sHostnameOrIPAddress,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uRemotePortNumber),
    [
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sRemoteIPAddress,
    ] if sHostnameOrIPAddress.lower() != sRemoteIPAddress.lower() else [],
    COLOR_NORMAL, " terminated.",
  );
