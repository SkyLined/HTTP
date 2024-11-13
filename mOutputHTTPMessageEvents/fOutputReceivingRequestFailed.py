from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_WARNING,
  STR_RECEIVING_REQUEST_ERROR3, STR_RECEIVING_REQUEST_SECURELY_ERROR3,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputReceivingRequestFailed(sToChar, sFromChar, sFromDescription, oConnection, oException):
  oConsole.fStatus(
    COLOR_ACTIVE,       sToChar,
    COLOR_ERROR,        STR_RECEIVING_REQUEST_SECURELY_ERROR3 if oConnection.bSecure else STR_RECEIVING_REQUEST_ERROR3,
    COLOR_ACTIVE,       sFromChar,
    COLOR_NORMAL,       " Receiving request ",
    [
      COLOR_INFO,       "securely",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text",
    ],
    COLOR_NORMAL,       " from ", sFromDescription, " ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       " failed.",
  );
  oConsole.fOutput(
    COLOR_NORMAL,       "     ",
    COLOR_INFO,         str(oException),
  );
