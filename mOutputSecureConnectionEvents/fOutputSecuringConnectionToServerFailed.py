from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INACTIVE,
  COLOR_NORMAL,
  STR_SECURING_ERROR3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fOutputSecuringConnectionFailed import fOutputSecuringConnectionFailed;

def fOutputSecuringConnectionToServerFailed(oHTTPClient, oException, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      STR_SECURING_ERROR3,
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection to the server failed.",
  );
  fOutputSecuringConnectionFailed(
    "     ",
    oException,
    "%s:%d" % (fsCP437FromBytesString(sbHost), uPortNumber),
  );
