from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST, 
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING,
  STR_SENDING_REQUEST3, STR_SENDING_REQUEST_SECURELY3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputSendingRequest(sFromChar, sToChar, sToDescription, oConnection, oRequest):
  oConsole.fStatus(
    COLOR_ACTIVE,       sFromChar,
    COLOR_REQUEST,      STR_SENDING_REQUEST_SECURELY3 if oConnection.bSecure else STR_SENDING_REQUEST3,
    COLOR_ACTIVE,       sToChar,
    COLOR_NORMAL,       " Sending ",
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_NORMAL,       " request (",
    COLOR_INFO,         fsBytesToHumanReadableString(len(oRequest.fsbSerialize())),
    COLOR_NORMAL,       ") ",
    [
      COLOR_INFO,       "securely",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text",
    ],
    COLOR_NORMAL,       " to ", sToDescription, " at ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL,       "...",
  );
