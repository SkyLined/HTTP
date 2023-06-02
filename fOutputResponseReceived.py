from faxListOutput import faxListOutput;
from foConsoleLoader import foConsoleLoader;
from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mColorsAndChars import \
    COLOR_CRLF, CHAR_CRLF, \
    COLOR_EOF, CHAR_EOF, \
    COLOR_NORMAL, \
    COLOR_RESPONSE_STATUS_LINE_1XX, \
    COLOR_RESPONSE_STATUS_LINE_2XX, \
    COLOR_RESPONSE_STATUS_LINE_3XX, \
    COLOR_RESPONSE_STATUS_LINE_4XX, \
    COLOR_RESPONSE_STATUS_LINE_5XX, \
    COLOR_RESPONSE_STATUS_LINE_INVALID, \
    COLOR_REQUEST_RESPONSE_BOX, \
    COLOR_REQUEST_RESPONSE_BOX_HEADER, \
    COLOR_WARNING, CHAR_WARNING;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputResponseReceived(oResponse, bShowDetails, bDecodeBody, bFixDecodeBodyErrors, xPrefix = []):
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
    COLOR_RESPONSE_STATUS_LINE, fsCP437FromBytesString(oResponse.fsbGetStatusLine()),
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
  );
  # Output response headers
  fOutputHeaders(
    oResponse.oHeaders,
    bShowDetails = bShowDetails,
    xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
  );
  oConsole.fOutput(
    xPrefix,
    [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
    [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    [COLOR_EOF, CHAR_EOF] if bShowDetails and not oResponse.sb0Body and not oResponse.o0AdditionalHeaders else [],
  );
  # Output response body if any
  if oResponse.sb0Body:
    fOutputBody(
      oResponse.fs0GetData(
        bTryOtherCompressionTypesOnFailure = bFixDecodeBodyErrors,
        bIgnoreDecompressionFailures = bFixDecodeBodyErrors,
      ) if bDecodeBody else oResponse.sb0Body,
      bNeedsDecoding = False if bDecodeBody else (oResponse.bChunked or oResponse.bCompressed),
      bShowDetails = bShowDetails,
      bOutputEOF = not oResponse.o0AdditionalHeaders,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
    );
  if oResponse.o0AdditionalHeaders:
    # Output response additional headers
    fOutputHeaders(
      oResponse.o0AdditionalHeaders,
      bShowDetails = bShowDetails,
      xPrefix = [xPrefix, COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else xPrefix,
    );
    oConsole.fOutput(
      xPrefix,
      [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
      [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
      [COLOR_EOF, CHAR_EOF] if bShowDetails else [],
    );
  if oResponse.asbActualCompressionTypes != oResponse.asbCompressionTypes:
    if oResponse.asbActualCompressionTypes:
      oConsole.fOutput(
        xPrefix,
        [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
        COLOR_WARNING, CHAR_WARNING, " NOTE",
        COLOR_NORMAL, ": The body was compressed using ",
        faxListOutput(
          asData = [str(sbCompressionType, "ascii", "strict") for sbCompressionType in oResponse.asbActualCompressionTypes],
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
