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
from .fOutputHTTPMessageData import fOutputHTTPMessageData;
from .fOutputHTTPMessageHeaders import fOutputHTTPMessageHeaders;

def fOutputHTTPRequest(
  oRequest,
  *,
  bShowDetails = None,
  bDecodeBody = None,
  bFailOnDecodeBodyErrors = None,
  bForceHexOutputOfBody = False,
  uHexOutputCharsPerLine = 16,
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
    COLOR_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
  );
  # Output request headers
  fOutputHTTPMessageHeaders(
    oRequest.oHeaders,
    bShowDetails = bShowDetails,
    xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
  );
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    [COLOR_EOF, CHAR_EOF] if bShowDetails and not oRequest.sb0Body and not oRequest.o0AdditionalHeaders else [],
  );
  # Output request body if any
  if oRequest.sb0Body:
    if bDecodeBody:
      fOutputHTTPMessageData(
        oRequest.fs0GetData(
          bTryOtherCompressionTypesOnFailure = not bFailOnDecodeBodyErrors,
          bIgnoreDecompressionFailures = not bFailOnDecodeBodyErrors,
        ),
        bShowDetails = bShowDetails,
        bOutputEOF = not oRequest.o0AdditionalHeaders,
        xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
      );
    else:
      fOutputHTTPMessageBody(
        oRequest.sb0Body,
        bShowDetails = bShowDetails,
        bOutputEOF = not oRequest.o0AdditionalHeaders,
        bForceHexOutput = bForceHexOutputOfBody,
        uHexOutputCharsPerLine = uHexOutputCharsPerLine,
        xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
      );
  if oRequest.o0AdditionalHeaders:
    # Output response additional headers
    fOutputHTTPMessageHeaders(
      oRequest.o0AdditionalHeaders,
      bShowDetails = bShowDetails,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
    );
    oConsole.fOutput(
      xPrefix,
      [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
      [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
      [COLOR_EOF, CHAR_EOF] if bShowDetails else [],
    );
  if oRequest.asbCompressionTypes and oRequest.asbActualCompressionTypes != oRequest.asbCompressionTypes:
    if oRequest.asbActualCompressionTypes:
      oConsole.fOutput(
        xPrefix,
        [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
        COLOR_WARNING, CHAR_WARNING, " NOTE",
        COLOR_NORMAL, ": The body was compressed using ",
        faxListOutput(
          asData = [str(sbCompressionType, "ascii", "strict") for sbCompressionType in oRequest.asbActualCompressionTypes],
          sAndOr = "and",
        ),
        COLOR_NORMAL, " compression!",
      );
    else:
      oConsole.fOutput(
        xPrefix,
        [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
        COLOR_WARNING, CHAR_WARNING, " NOTE",
        COLOR_NORMAL, ": The body could not be decompressed!",
      );
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "└" if bShowDetails else "─", sPadding = "─",
  );
