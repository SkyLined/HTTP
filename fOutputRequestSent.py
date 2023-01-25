from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputRequestSent(oRequest, bShowDetails, bDecodeBody, xPrefix = []):
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "┌───[",
    COLOR_REQUEST_RESPONSE_BOX_HEADER, " Request ",
    COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
  );
  # Output request status line
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "│ ", 
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    COLOR_CRLF, CHAR_CRLF,
  );
  if bShowDetails:
    # Output request headers
    fOutputHeaders(
      oRequest.oHeaders,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
    );
    oConsole.fOutput(
      xPrefix,
      COLOR_REQUEST_RESPONSE_BOX, "│ ", 
      COLOR_CRLF, CHAR_CRLF,
      *([COLOR_EOF, CHAR_EOF] if not oRequest.sb0Body is not None else [])
    );
    if oRequest.sb0Body:
      if bDecodeBody:
        # Output decoded request body if any
        fOutputBody(
          oRequest.s0Data,
          bOutputEOF = not oRequest.o0AdditionalHeaders,
          xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
        );
      else:
        # Output request body if any
        fOutputBody(oRequest.sb0Body, bOutputEOF = not oRequest.o0AdditionalHeaders);
    if oRequest.o0AdditionalHeaders:
      # Output response additional headers
      fOutputHeaders(
        oRequest.o0AdditionalHeaders,
        xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
      );
      oConsole.fOutput(
        xPrefix,
        COLOR_REQUEST_RESPONSE_BOX, "│ ", 
        COLOR_CRLF, CHAR_CRLF,
        COLOR_EOF, CHAR_EOF,
      );
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "└", sPadding = "─",
  );
