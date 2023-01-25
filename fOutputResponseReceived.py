from foConsoleLoader import foConsoleLoader;
from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputResponseReceived(oResponse, bShowDetails, bDecodeBody, xPrefix = []):
  if 100 <= oResponse.uStatusCode <= 199:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_1XX;
  elif 200 <= oResponse.uStatusCode <= 299:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_2XX;
  elif 300 <= oResponse.uStatusCode <= 399:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_3XX;
  elif 400 <= oResponse.uStatusCode <= 499:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_4XX;
  elif 500 <= oResponse.uStatusCode <= 599:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_5XX;
  else:
    COLOR_RESPONSE_STATUS_LINE = COLOR_RESPONSE_STATUS_LINE_INVALID;
  
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "┌───[",
    COLOR_REQUEST_RESPONSE_BOX_HEADER, " Response ",
    COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
  );
  ### OUTPUT RESPONSE ####################################################
  # Output response status line
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "│ ", 
    COLOR_RESPONSE_STATUS_LINE, fsCP437FromBytesString(oResponse.fsbGetStatusLine()),
    COLOR_CRLF, CHAR_CRLF,
  );
  if bShowDetails:
    fOutputHeaders(
      oResponse.oHeaders,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
    );
    oConsole.fOutput(
      xPrefix,
      COLOR_REQUEST_RESPONSE_BOX, "│ ", 
      COLOR_CRLF, CHAR_CRLF,
      *([COLOR_EOF, CHAR_EOF] if not oResponse.sb0Body and not oResponse.o0AdditionalHeaders else [])
    );
  # Output response body if any
  if oResponse.sb0Body:
    fOutputBody(
      oResponse.s0Data if bDecodeBody else oResponse.sb0Body,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
      bOutputEOF = not oResponse.o0AdditionalHeaders,
    );
  if bShowDetails and oResponse.o0AdditionalHeaders:
    # Output response additional headers
    fOutputHeaders(
      oResponse.o0AdditionalHeaders,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "],
    );
    oConsole.fOutput(
      xPrefix,
      COLOR_REQUEST_RESPONSE_BOX, "│ ", 
      COLOR_CRLF, CHAR_CRLF,
      COLOR_EOF, CHAR_EOF,
    );
  oConsole.fOutput(
    COLOR_REQUEST_RESPONSE_BOX, "└", sPadding = "─",
  );
