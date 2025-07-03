from faxListOutput import faxListOutput;
from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_CRLF, CHAR_CRLF,
  COLOR_EOF, CHAR_EOF,
  COLOR_NORMAL,
  COLOR_REQUEST_RESPONSE_BOX,
  COLOR_REQUEST_RESPONSE_BOX_HEADER,
  COLOR_REQUEST_STATUS_LINE,
  COLOR_WARNING, CHAR_WARNING,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

from .fOutputHTTPMessageBody import fOutputHTTPMessageBody;
from .fOutputHTTPMessageHeadersOrTrailers import fOutputHTTPMessageHeadersOrTrailers;

def fOutputHTTPRequest(
  oRequest,
  *,
  bShowDetails: bool,
  bShowMessageBody: bool,
  bDecodeBody,
  bFailOnDecodeBodyErrors,
  bForceHexOutputOfBody,
  uHexOutputCharsPerLine,
  xPrefix = [],
):
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "┌" if bShowDetails else "─", "───[",
    COLOR_REQUEST_RESPONSE_BOX_HEADER, " Request ",
    COLOR_REQUEST_RESPONSE_BOX, "]", sPadding = "─",
  );
  # Output request status line
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStartLine()),
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
  );
  # Output request headers
  fOutputHTTPMessageHeadersOrTrailers(
    oRequest.oHeaders,
    bShowDetails = bShowDetails,
    xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
  );
  # Output headers/body separator:
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    [COLOR_EOF, CHAR_EOF] if bShowDetails and not oRequest.sbBody else [],
  );
  # Output request body if any
  if bShowMessageBody and oRequest.sbBody:
    fOutputHTTPMessageBody(
      oMessage = oRequest,
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
