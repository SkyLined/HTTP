from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR, STR_SECURING_ERROR3,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;
from .fOutputSecuringConnectionExceptionDetails import fOutputSecuringConnectionExceptionDetails;

def fOutputToServerFromClientSecuringConnectionFailed(oHTTPClient_unused, *, oConnection, oSSLContext, oException):
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_ERROR,        STR_SECURING_ERROR3,
    COLOR_NORMAL,       "C",
    COLOR_NORMAL,       " Securing connection from client ",
    fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber),
    COLOR_NORMAL,       " failed.",
  );
  fOutputSecuringConnectionExceptionDetails(
    "      ",
    oException,
    "%s:%d" % (oConnection.sbRemoteHost, oConnection.uRemotePortNumber),
  );
