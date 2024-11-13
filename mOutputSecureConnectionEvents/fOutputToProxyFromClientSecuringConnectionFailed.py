from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR, CHAR_SECURING_ERROR,
  COLOR_INACTIVE,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;
from .fOutputSecuringConnectionExceptionDetails import fOutputSecuringConnectionExceptionDetails;

def fOutputToProxyFromClientSecuringConnectionFailed(oHTTPClient, *, oConnection, oSSLContext, oException):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_SECURING_ERROR,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,     " failed.",
  );
  fOutputSecuringConnectionExceptionDetails(
    "      ",
    oException,
    "%s:%d" % (fsCP437FromBytesString(oConnection.sbRemoteHost), oConnection.uRemotePortNumber),
  );
