from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED, CHAR_CONNECTED_TO,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_RESPONSE,
  COLOR_WARNING,
  CHAR_RECEIVING_RESPONSE, STR_RECEIVING_RESPONSE3,
  CHAR_RECEIVING_RESPONSE_SECURELY, STR_RECEIVING_RESPONSE_SECURELY3,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputReceivingResponse(oConnection, oRequest, o0ProxyServerURL):
  bIsConnectRequest = oRequest.sbMethod.upper() == b"CONNECT";
  oConsole.fStatus(
    [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     STR_RECEIVING_RESPONSE_SECURELY3 if oConnection.bSecure else STR_RECEIVING_RESPONSE3,
      COLOR_ACTIVE,       "S",
    ] if o0ProxyServerURL is None else [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     CHAR_RECEIVING_RESPONSE_SECURELY if oConnection.bSecure else CHAR_RECEIVING_RESPONSE,
      COLOR_ACTIVE,       "P",
      COLOR_CONNECTED,    CHAR_CONNECTED_TO,
      COLOR_INACTIVE,     "S",
    ] if bIsConnectRequest else [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     CHAR_RECEIVING_RESPONSE_SECURELY if oConnection.bSecure else CHAR_RECEIVING_RESPONSE,
      COLOR_ACTIVE,       "P",
      COLOR_RESPONSE,      CHAR_RECEIVING_RESPONSE,
      COLOR_ACTIVE,       "S",
    ],
    COLOR_NORMAL, " Receiving response ",
    [
      COLOR_INFO, "securely ",
    ] if oConnection.bSecure else [
      COLOR_WARNING, "in plain text ",
    ],
    COLOR_NORMAL,
    [
      "through proxy server at ",
      COLOR_INFO, fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute),
    ] if o0ProxyServerURL else [
      "from server at ",
      COLOR_INFO, fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute)
    ],
    COLOR_NORMAL, "...",
  );
