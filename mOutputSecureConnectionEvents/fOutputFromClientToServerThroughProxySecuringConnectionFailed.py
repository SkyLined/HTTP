from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR, CHAR_SECURING_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fasOutputAddress import fasOutputAddress;

def fOutputFromClientToServerThroughProxySecuringConnectionFailed(oHTTPClient_unused, *, oProxyServerURL, oConnection, sbServerHost, uServerPortNumber, oSSLContext, uStatusCode):
  oConsole.fOutput(
    COLOR_ACTIVE,     "C",
    COLOR_ERROR,      CHAR_SECURING_ERROR,
    COLOR_ACTIVE,     "P",
    COLOR_ERROR,      CHAR_SECURING_ERROR,
    COLOR_ACTIVE,     "S",
    COLOR_NORMAL,     " Securing connection to server ",
    fasOutputAddress(sbHost = sbServerHost, uPortNumber = uServerPortNumber),
    COLOR_NORMAL,     " through proxy ",
    fasOutputAddress(sbHost = oProxyServerURL.sbHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oProxyServerURL.uPortNumber),
    COLOR_NORMAL,     " failed with status code ",
    COLOR_INFO,       str(uStatusCode),
    COLOR_NORMAL,     ".",
  );
