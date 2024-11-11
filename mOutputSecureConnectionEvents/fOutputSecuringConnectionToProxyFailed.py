from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INACTIVE,
  COLOR_NORMAL,
  CHAR_SECURING_ERROR,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fOutputSecuringConnectionFailed import fOutputSecuringConnectionFailed;

def fOutputSecuringConnectionToProxyFailed(oHTTPClient, oException, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_SECURING_ERROR,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection to the proxy server failed.",
  );
  fOutputSecuringConnectionFailed(
    "      ",
    oException,
    "%s:%d" % (fsCP437FromBytesString(sbHost), uPortNumber),
  );
