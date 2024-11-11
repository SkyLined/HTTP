from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST,
  COLOR_WARNING,
  STR_RECEIVING_REQUEST3, STR_RECEIVING_REQUEST_SECURELY3
);
oConsole = foConsoleLoader();

def fOutputReceivingRequest(oConnection):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fStatus(
    COLOR_ACTIVE,       "S",
    COLOR_REQUEST,      STR_RECEIVING_REQUEST_SECURELY3 if oConnection.bSecure else STR_RECEIVING_REQUEST3,
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL,       " Receiving request ",
    [
      COLOR_INFO,       "securely ",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text ",
    ],
    COLOR_NORMAL,       "from client at ",
    COLOR_INFO,         sRemoteIPAddress,
    COLOR_NORMAL,       ":",
    COLOR_INFO,         str(uRemotePortNumber),
    COLOR_NORMAL,       ".",
  );
