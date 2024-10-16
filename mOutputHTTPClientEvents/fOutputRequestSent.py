from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECT,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_REQUEST,
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputRequestSent(oConnection, oRequest, o0ProxyServerURL, bShowProxyConnects):
  bIsConnectRequest = oRequest.sbMethod.upper() == b"CONNECT";
  if bIsConnectRequest and not bShowProxyConnects:
    return;
  oConsole.fOutput(
    [
      COLOR_ACTIVE,       "C",
      COLOR_REQUEST,      "==►" if oConnection.bSecure else "--►",
      COLOR_ACTIVE,       "S",
    ] if o0ProxyServerURL is None else [
      COLOR_ACTIVE,       "C",
      COLOR_REQUEST,      "►",
      COLOR_ACTIVE,       "P",
      COLOR_CONNECT,      "→",
      COLOR_INACTIVE,     "S",
    ] if bIsConnectRequest else [
      COLOR_ACTIVE,       "C",
      COLOR_REQUEST,      "►",
      COLOR_ACTIVE,       "P",
      COLOR_REQUEST,      "►",
      COLOR_ACTIVE,       "S",
    ],
    COLOR_NORMAL, " Sent ",
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_NORMAL, " request (",
    COLOR_INFO, fsBytesToHumanReadableString(len(oRequest.fsbSerialize())),
    COLOR_NORMAL, ") ",
    [
      COLOR_INFO, "securely ",
    ] if oConnection.bSecure else [
      COLOR_WARNING, "in plain text ",
    ],
    COLOR_NORMAL,
    [
      "to" if bIsConnectRequest else "through",
      " proxy server at ",
      COLOR_INFO, fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute),
    ] if o0ProxyServerURL else [
      "to server at ",
      COLOR_INFO, fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute),
    ],
    COLOR_NORMAL, ".",
  );
