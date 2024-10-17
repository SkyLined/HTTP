from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_CONNECTED,
  COLOR_INACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_RESPONSE_1XX, COLOR_RESPONSE_STATUS_LINE_1XX,
  COLOR_RESPONSE_2XX, COLOR_RESPONSE_STATUS_LINE_2XX,
  COLOR_RESPONSE_3XX, COLOR_RESPONSE_STATUS_LINE_3XX,
  COLOR_RESPONSE_4XX, COLOR_RESPONSE_STATUS_LINE_4XX,
  COLOR_RESPONSE_5XX, COLOR_RESPONSE_STATUS_LINE_5XX,
  COLOR_RESPONSE_INVALID, COLOR_RESPONSE_STATUS_LINE_INVALID,
  COLOR_WARNING,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputResponseReceived(oConnection, oRequest, oResponse, o0ProxyServerURL):
  bIsConnectRequest = oRequest.sbMethod.upper() == b"CONNECT";
  if 100 <= oResponse.uStatusCode <= 199:
    COLOR_RESPONSE = COLOR_RESPONSE_1XX;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_1XX;
  elif 200 <= oResponse.uStatusCode <= 299:
    COLOR_RESPONSE = COLOR_RESPONSE_2XX;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_2XX;
  elif 300 <= oResponse.uStatusCode <= 399:
    COLOR_RESPONSE = COLOR_RESPONSE_3XX;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_3XX;
  elif 400 <= oResponse.uStatusCode <= 499:
    COLOR_RESPONSE = COLOR_RESPONSE_4XX;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_4XX;
  elif 500 <= oResponse.uStatusCode <= 599:
    COLOR_RESPONSE = COLOR_RESPONSE_5XX;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_5XX;
  else:
    COLOR_RESPONSE = COLOR_RESPONSE_INVALID;
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_INVALID;
  
  sb0MediaType = oResponse.sb0MediaType; # Getter; this takes time, so cache it.
  oConsole.fOutput(
    [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     "◄", "══" if oConnection.bSecure else "--",
      COLOR_ACTIVE,       "S",
    ] if o0ProxyServerURL is None else [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     "◄",
      COLOR_ACTIVE,       "P",
      COLOR_CONNECTED,    "→",
      COLOR_INACTIVE,     "S",
    ] if bIsConnectRequest else [
      COLOR_ACTIVE,       "C",
      COLOR_RESPONSE,     "◄",
      COLOR_ACTIVE,       "P",
      COLOR_RESPONSE,     "◄",
      COLOR_ACTIVE,       "S",
    ],
    COLOR_NORMAL, " Received ",
    COLOR_RESPONSE_STATUS_LINE, fsCP437FromBytesString(oResponse.fsbGetStatusLine()),
    COLOR_NORMAL, " response (",
    COLOR_INFO, fsBytesToHumanReadableString(len(oResponse.fsbSerialize())),
    COLOR_NORMAL,
    [
      " ", fsCP437FromBytesString(sb0MediaType),
    ] if sb0MediaType else [],
    ") ",
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
    COLOR_NORMAL, ".",
  );
