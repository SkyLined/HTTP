from mConsole import oConsole;
from mHumanReadable import fsBytesToHumanReadableString;

from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputRequestSent(oConnection, oRequest, o0ProxyServerURL, bShowProgress, bShowRequest, bShowDetails, bDecodeBody):
  if bShowProgress:
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Sent ",
      COLOR_INFO, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
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
        "through proxy server at ",
        COLOR_INFO, fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute),
      ] if o0ProxyServerURL else [
        "to server at ",
        COLOR_INFO, fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute),
      ],
      COLOR_NORMAL, ".",
    );
  oConsole.fOutput(
    COLOR_REQUEST_RESPONSE_BOX, "┌───[", COLOR_REQUEST_RESPONSE_BOX_HEADER, " Request ", COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
  );
  # Output request status line
  oConsole.fOutput(
    COLOR_REQUEST_RESPONSE_BOX, "│ ", 
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_CRLF, CHAR_CRLF,
  );
  if bShowDetails:
    # Output request headers
    fOutputHeaders(oRequest.oHeaders);
    oConsole.fOutput(
      COLOR_REQUEST_RESPONSE_BOX, "│ ", 
      COLOR_CRLF, CHAR_CRLF,
      *([COLOR_EOF, CHAR_EOF] if not oRequest.sb0Body is not None else [])
    );
    if oRequest.sb0Body:
      if bDecodeBody:
        # Output decoded request body if any
        fOutputBody(oRequest.s0Data, bOutputEOF = not oRequest.o0AdditionalHeaders);
      else:
        # Output request body if any
        fOutputBody(oRequest.sb0Body, bOutputEOF = not oRequest.o0AdditionalHeaders);
    if oRequest.o0AdditionalHeaders:
      # Output response additional headers
      fOutputHeaders(oRequest.o0AdditionalHeaders);
      oConsole.fOutput(
        COLOR_REQUEST_RESPONSE_BOX, "│ ", 
        COLOR_CRLF, CHAR_CRLF,
        COLOR_EOF, CHAR_EOF,
      );
  oConsole.fOutput(
    COLOR_REQUEST_RESPONSE_BOX, "└", sPadding = "─",
  );
