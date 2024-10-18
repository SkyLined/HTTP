from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST,
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputRequestReceived(oConnection, oRequest):
  (sRemoteIPAddress, uRemotePortNumber) = oConnection.txRemoteAddress[:2];
  oConsole.fOutput(
    COLOR_ACTIVE,       "S",
    COLOR_REQUEST,      "◄", "══" if oConnection.bSecure else "--",
    COLOR_ACTIVE,       "C",
    COLOR_NORMAL, " Received ",
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_NORMAL, " request (",
    COLOR_INFO, fsBytesToHumanReadableString(len(oRequest.fsbSerialize())),
    COLOR_NORMAL, ") ",
    [
      COLOR_INFO, "securely ",
    ] if oConnection.bSecure else [
      COLOR_WARNING, "in plain text ",
    ],
    COLOR_NORMAL, "from client at ",
    COLOR_INFO, sRemoteIPAddress,
    COLOR_NORMAL, ":",
    COLOR_INFO, str(uRemotePortNumber),
    COLOR_NORMAL, ".",
  );
