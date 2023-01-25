from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import fbIsProvided;
oConsole = foConsoleLoader();

def fHandleConnectingToServerIPAddressFailed(oHTTPClient, oException, sbHostnameOrIPAddress, sIPAddress, uPortNumber, sbzHostname):
  # We only show this message if the user provided a hostname instead of an IP address.
  if fbIsProvided(sbzHostname):
    sHostnameOrIPAddress = fsCP437FromBytesString(sbHostnameOrIPAddress);
    oConsole.fOutput(
      COLOR_ACTIVE,     "C",
      COLOR_ERROR,      "-×→",
      COLOR_NORMAL,     "S",
      COLOR_NORMAL, " Connecting to server ",
      COLOR_INFO, ("[%s]" if ":" in sHostnameOrIPAddress else "%s") % sHostnameOrIPAddress,
      COLOR_NORMAL, ":",
      COLOR_INFO, str(uPortNumber),
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
      COLOR_NORMAL, "!",
    );
    oConsole.fOutput(
      "    ",
      COLOR_INFO, CHAR_INFO, 
      COLOR_NORMAL, " ",
      COLOR_HILITE, str(oException.sMessage),
      COLOR_NORMAL, ".",
    );

