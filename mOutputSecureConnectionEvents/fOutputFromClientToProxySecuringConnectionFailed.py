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

def fOutputFromClientToProxySecuringConnectionFailed(oHTTPClient, *, oProxyServerURL, sbHost, sbIPAddress, uPortNumber, oConnection, oSSLContext, oException):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_SECURING_ERROR,
    COLOR_NORMAL,     "P",
    COLOR_NORMAL,     " ",
    COLOR_INACTIVE,   "S",
    COLOR_NORMAL,     " Securing the connection to the proxy server ",
    fasOutputAddress(sbHost = sbHost, sbIPAddress = sbIPAddress, uPortNumber = uPortNumber),
    COLOR_NORMAL,     " failed.",
  );
  fOutputSecuringConnectionExceptionDetails(
    "      ",
    oException,
    "%s:%d" % (fsCP437FromBytesString(sbHost), uPortNumber),
  );
