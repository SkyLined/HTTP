from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
  STR_SECURING_ERROR3,
);
oConsole = foConsoleLoader();

from .fOutputSecuringConnectionFailed import fOutputSecuringConnectionFailed;

def fOutputSecuringConnectionFromClientFailed(oHTTPClient_unused, oConnection, oSSLContext, oException):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_ERROR,        STR_SECURING_ERROR3,
    COLOR_NORMAL,       "C",
    COLOR_NORMAL,       " Securing connection from client ",
    COLOR_INFO,         sRemoteIPAddress,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    COLOR_NORMAL,       " failed.",
  );
  fOutputSecuringConnectionFailed(
    "      ",
    oException,
    "%s:%d" % (sRemoteIPAddress, uRemotePortNumber),
  );
