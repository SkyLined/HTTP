from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTING, CHAR_CONNECTING_TO,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST,
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING,
  CHAR_SENDING_REQUEST, STR_SENDING_REQUEST3,
  CHAR_SENDING_REQUEST_SECURELY, STR_SENDING_REQUEST_SECURELY3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputSendingRequest(oConnection, oRequest, o0ProxyServerURL):
  bIsConnectRequest = oRequest.sbMethod.upper() == b"CONNECT";
  oConsole.fStatus(
    [
      COLOR_ACTIVE,     "C",
      COLOR_REQUEST,    STR_SENDING_REQUEST_SECURELY3 if oConnection.bSecure else STR_SENDING_REQUEST3,
      COLOR_ACTIVE,     "S",
    ] if o0ProxyServerURL is None else [
      COLOR_ACTIVE,     "C",
      COLOR_REQUEST,    CHAR_SENDING_REQUEST_SECURELY if oConnection.bSecure else CHAR_SENDING_REQUEST,
      COLOR_ACTIVE,     "P",
      COLOR_REQUEST,    CHAR_SENDING_REQUEST,
      COLOR_INACTIVE,   "S",
    ] if bIsConnectRequest else [
      COLOR_ACTIVE,     "C",
      COLOR_REQUEST,    CHAR_SENDING_REQUEST_SECURELY if oConnection.bSecure else CHAR_SENDING_REQUEST,
      COLOR_ACTIVE,     "P",
      COLOR_CONNECTING, CHAR_CONNECTING_TO,
      COLOR_ACTIVE,     "S",
    ],
    COLOR_NORMAL,       " Sending ",
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_NORMAL,       " request (",
    COLOR_INFO,         fsBytesToHumanReadableString(len(oRequest.fsbSerialize())),
    COLOR_NORMAL,       ") ",
    [
      COLOR_INFO,       "securely ",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text ",
    ],
    COLOR_NORMAL,
    [
                        "to" if bIsConnectRequest else "through",
                        " proxy server at ",
      COLOR_INFO,       fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute),
    ] if o0ProxyServerURL else [
                        "to server at ",
      COLOR_INFO,       fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute),
    ],
    COLOR_NORMAL,       "...",
  );
