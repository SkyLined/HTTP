from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputConnectedToHostname(oConnection, sbHostname, sCanonicalName, sIPAddress):
  sHostname = fsCP437FromBytesString(sbHostname);
  if sHostname.lower() != sIPAddress.lower():
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Connect to hostname ",
      COLOR_INFO, sHostname,
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
      COLOR_NORMAL, ".",
    );
  elif not sCanonicalName.startswith("%s:" % sIPAddress):
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Connected to IP address ",
      COLOR_HILITE, sIPAddress,
      COLOR_NORMAL, ".",
    );
