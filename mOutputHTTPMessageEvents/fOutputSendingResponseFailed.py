﻿from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ACTIVE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_RESPONSE_1XX, COLOR_RESPONSE_STATUS_LINE_1XX,
  COLOR_RESPONSE_2XX, COLOR_RESPONSE_STATUS_LINE_2XX,
  COLOR_RESPONSE_3XX, COLOR_RESPONSE_STATUS_LINE_3XX,
  COLOR_RESPONSE_4XX, COLOR_RESPONSE_STATUS_LINE_4XX,
  COLOR_RESPONSE_5XX, COLOR_RESPONSE_STATUS_LINE_5XX,
  COLOR_RESPONSE_INVALID, COLOR_RESPONSE_STATUS_LINE_INVALID,
  COLOR_WARNING,
  STR_SENDING_RESPONSE_SECURELY3, STR_SENDING_RESPONSE3
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fasOutputRemoteAddressForConnection import fasOutputRemoteAddressForConnection;

def fOutputSendingResponseFailed(sFromChar, sToChar, sToDescription, oConnection, oResponse, oException):
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
    COLOR_ACTIVE,       sFromChar,
    COLOR_RESPONSE,     STR_SENDING_RESPONSE_SECURELY3 if oConnection.bSecure else STR_SENDING_RESPONSE3,
    COLOR_ACTIVE,       sToChar,
    COLOR_NORMAL,       " Sending ",
    COLOR_RESPONSE_STATUS_LINE, fsCP437FromBytesString(oResponse.fsbGetStartLine()),
    COLOR_NORMAL,       " response (",
    COLOR_INFO,         fsBytesToHumanReadableString(len(oResponse.fsbSerialize())),
    [
      COLOR_NORMAL,     " ",
      COLOR_INFO,       fsCP437FromBytesString(sb0MediaType),
    ] if sb0MediaType else [],
    COLOR_NORMAL,       ") ",  
    [
      COLOR_INFO,       "securely",
    ] if oConnection.bSecure else [
      COLOR_WARNING,    "in plain text",
    ],
    COLOR_NORMAL,       " to ", sToDescription, " ",
    fasOutputRemoteAddressForConnection(oConnection),
    COLOR_NORMAL, " failed.",
  );
  oConsole.fOutput(
    COLOR_NORMAL,       "     ",
    COLOR_INFO,         str(oException),
  );
