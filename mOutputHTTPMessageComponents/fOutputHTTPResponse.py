from faxListOutput import faxListOutput;
from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_CRLF, CHAR_CRLF,
  COLOR_EOF, CHAR_EOF,
  COLOR_NORMAL,
  COLOR_RESPONSE_STATUS_LINE_1XX,
  COLOR_RESPONSE_STATUS_LINE_2XX,
  COLOR_RESPONSE_STATUS_LINE_3XX,
  COLOR_RESPONSE_STATUS_LINE_4XX,
  COLOR_RESPONSE_STATUS_LINE_5XX,
  COLOR_RESPONSE_STATUS_LINE_INVALID,
  COLOR_REQUEST_RESPONSE_BOX,
  COLOR_REQUEST_RESPONSE_BOX_HEADER,
  COLOR_WARNING, CHAR_WARNING,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fOutputHTTPMessageBody import fOutputHTTPMessageBody;
from .fOutputHTTPMessageHeadersOrTrailers import fOutputHTTPMessageHeadersOrTrailers;

def fOutputHTTPResponse(
    oResponse,
    *,
    bDecodeBody,
    bFailOnDecodeBodyErrors,
    bForceHexOutputOfBody,
    bShowDetails,
    bShowMessageBody,
    uHexOutputCharsPerLine,
    xPrefix = [],
  ):
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
    COLOR_REQUEST_RESPONSE_BOX, "┌" if bShowDetails else "─", "───[",
    COLOR_REQUEST_RESPONSE_BOX_HEADER, " Response ",
    COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
  );
  ### OUTPUT RESPONSE ####################################################
  # Output response status line
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    COLOR_RESPONSE_STATUS_LINE, fsCP437FromBytesString(oResponse.fsbGetStartLine()),
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
  );
  # Output response headers
  fOutputHTTPMessageHeadersOrTrailers(
    oResponse.oHeaders,
    bShowDetails = bShowDetails,
    xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
  );
  # Output headers/body separator:
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    [COLOR_EOF, CHAR_EOF] if bShowDetails and not oResponse.sbBody else [],
  );
  # Output response body if any
  if bShowMessageBody:
    fOutputHTTPMessageBody(
      oMessage = oResponse,
      bDecodeBody = bDecodeBody,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bShowDetails = bShowDetails,
      bForceHexOutput = bForceHexOutputOfBody,
      uHexOutputCharsPerLine = uHexOutputCharsPerLine,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
    );
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "└" if bShowDetails else "─", sPadding = "─",
  );
