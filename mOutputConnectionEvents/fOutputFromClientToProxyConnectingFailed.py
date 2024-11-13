from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_HILITE,
  COLOR_INACTIVE,
  COLOR_INFO, CHAR_INFO,
  COLOR_NORMAL,
  CHAR_CONNECTING_TO_ERROR,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToProxyConnectingFailed(oHTTPClient_unused, *, oProxyServerURL, sbIPAddress, uPortNumber, oException):
  sIPAddress = fsCP437FromBytesString(sbIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_CONNECTING_TO_ERROR,
    COLOR_ERROR,      "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Connecting to proxy ",
    fasOutputAddress(sbHost = oProxyServerURL.sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     " failed!",
  );
  oConsole.fOutput(
    "    ",
    COLOR_INFO, CHAR_INFO, 
    COLOR_NORMAL, " ",
    COLOR_HILITE, str(oException.sMessage),
    COLOR_NORMAL, ".",
  );

