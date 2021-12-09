from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fHandleServerHostnameOrIPAddressInvalid(oHTTPClient, sbHostnameOrIPAddress):
  sHostnameOrIPAddress = fsCP437FromBytesString(sbHostnameOrIPAddress);
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      "·×·",
    COLOR_ERROR,      "S",
    COLOR_NORMAL, " The server name or IP address ",
    COLOR_INFO, sHostnameOrIPAddress,
    COLOR_NORMAL, " is not valid!",
  );
