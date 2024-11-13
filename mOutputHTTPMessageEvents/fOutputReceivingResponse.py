from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_RESPONSE,
  COLOR_WARNING,
  STR_RECEIVING_RESPONSE3, STR_RECEIVING_RESPONSE_SECURELY3,
);
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputReceivingResponse(sToChar, sFromChar, sFromDescription, oConnection):
  oConsole.fStatus(
    COLOR_ACTIVE,       sToChar,
    COLOR_RESPONSE,     STR_RECEIVING_RESPONSE_SECURELY3 if oConnection.bSecure else STR_RECEIVING_RESPONSE3,
    COLOR_ACTIVE,       sFromChar,
    COLOR_NORMAL,       " Receiving response ",
    [
      COLOR_INFO,       "securely",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text",
    ],
    COLOR_NORMAL,       " from ", sFromDescription, " ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL, "...",
  );
