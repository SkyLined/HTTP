from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_ERROR, 
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING,
  STR_SENDING_REQUEST_ERROR3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputSendingRequestFailed(sFromChar, sToChar, sToDescription, oConnection, oRequest, oException):
  oConsole.fStatus(
    COLOR_ACTIVE,       sFromChar,
    COLOR_ERROR,        STR_SENDING_REQUEST_ERROR3,
    COLOR_ACTIVE,       sToChar,
    COLOR_NORMAL,       " Sending ",
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStartLine()),
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
    COLOR_NORMAL,       " failed.",
  );
  oConsole.fOutput(
    COLOR_NORMAL,       "     ",
    COLOR_INFO,         str(oException),
  );