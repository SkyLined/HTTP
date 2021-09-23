from mConsole import oConsole;
from mHumanReadable import fsBytesToHumanReadableString;

from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputResponseReceived(oConnection, oResponse, o0ProxyServerURL, bShowProgress, bShowResponse, bShowDetails, bDecodeBody):
  if bShowProgress:
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Received ",
      COLOR_INFO, fsCP437FromBytesString(oResponse.fsbGetStatusLine()),
      COLOR_NORMAL, " response (",
      COLOR_INFO, fsBytesToHumanReadableString(len(oResponse.fsbSerialize())),
      COLOR_NORMAL,
      [
        " ", fsCP437FromBytesString(oResponse.sb0MediaType),
      ] if oResponse.sb0MediaType else [],
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
  if bShowResponse:
    oConsole.fOutput(
      COLOR_REQUEST_RESPONSE_BOX, "┌───[", COLOR_REQUEST_RESPONSE_BOX_HEADER, " Response ", COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
    );
    ### OUTPUT RESPONSE ####################################################
    # Output response status line
    if 100 <= oResponse.uStatusCode < 200: 
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_1XX;
    elif 200 <= oResponse.uStatusCode < 300: 
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_2XX;
    elif 300 <= oResponse.uStatusCode < 400: 
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_3XX;
    elif 400 <= oResponse.uStatusCode < 500: 
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_4XX;
    elif 500 <= oResponse.uStatusCode < 600: 
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_5XX;
    else:
      xStatusLineColor = COLOR_RESPONSE_STATUS_LINE_INVALID;
    oConsole.fOutput(
      COLOR_REQUEST_RESPONSE_BOX, "│ ", 
      xStatusLineColor, fsCP437FromBytesString(oResponse.fsbGetStatusLine()),
      COLOR_CRLF, CHAR_CRLF,
    );
    if bShowDetails:
      fOutputHeaders(oResponse.oHeaders);
      oConsole.fOutput(
        COLOR_REQUEST_RESPONSE_BOX, "│ ", 
        COLOR_CRLF, CHAR_CRLF,
        *([COLOR_EOF, CHAR_EOF] if not oResponse.sb0Body and not oResponse.o0AdditionalHeaders else [])
      );
    # Output response body if any
    if oResponse.sb0Body:
      fOutputBody(oResponse.s0Data if bDecodeBody else oResponse.sb0Body, bOutputEOF = not oResponse.o0AdditionalHeaders);
    if bShowDetails and oResponse.o0AdditionalHeaders:
      # Output response additional headers
      fOutputHeaders(oResponse.o0AdditionalHeaders);
      oConsole.fOutput(
        COLOR_REQUEST_RESPONSE_BOX, "│ ", 
        COLOR_CRLF, CHAR_CRLF,
        COLOR_EOF, CHAR_EOF,
      );
    oConsole.fOutput(
      COLOR_REQUEST_RESPONSE_BOX, "└", sPadding = "─",
    );
