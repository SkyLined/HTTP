from faxListOutput import faxListOutput;
from foConsoleLoader import foConsoleLoader;
from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputRequestSent(oRequest, bShowDetails, bDecodeBody, bFixDecodeBodyErrors, xPrefix = []):
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
  fOutputHeaders(
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
    fOutputBody(
      oRequest.fs0GetData(
        bTryOtherCompressionTypesOnFailure = bFixDecodeBodyErrors,
        bIgnoreDecompressionFailures = bFixDecodeBodyErrors,
      ) if bDecodeBody else oRequest.sb0Body,
      bNeedsDecoding = False if bDecodeBody else (oRequest.bChunked or oRequest.bCompressed),
      asb0ActualCompressionTypesList = oRequest.asb0ActualCompressionTypes,
      bShowDetails = bShowDetails,
      bOutputEOF = not oRequest.o0AdditionalHeaders,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
    );
  if oRequest.o0AdditionalHeaders:
    # Output response additional headers
    fOutputHeaders(
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
  if oRequest.asb0ActualCompressionTypes:
    oConsole.fOutput(
      xPrefix,
      [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
      COLOR_ERROR, CHAR_ERROR, " NOTE",
      COLOR_NORMAL, ": The body was compressed using ",
      faxListOutput(
        asData = [str(sbCompressionType, "ascii", "strict") for sbCompressionType in oRequest.asb0ActualCompressionTypes],
        sAndOr = "and",
      ),
      COLOR_NORMAL, " compression!",
    );
  oConsole.fOutput(
    xPrefix,
    COLOR_REQUEST_RESPONSE_BOX, "└" if bShowDetails else "─", sPadding = "─",
  );
