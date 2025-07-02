from mHTTPProtocol import iMessage;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_DATA,
  COLOR_CR, CHAR_CR,
  COLOR_CRLF, CHAR_CRLF,
  COLOR_EOF, CHAR_EOF,
  COLOR_LF, CHAR_LF,
  COLOR_NORMAL,
  COLOR_REQUEST_RESPONSE_BOX,
  COLOR_WARNING, CHAR_WARNING,
);
oConsole = foConsoleLoader();

from .fOutputHTTPMessageHeadersOrTrailers import fOutputHTTPMessageHeadersOrTrailers;

def fOutputHTTPMessageBodyAsData(
  oMessage: iMessage,
  *,
  bShowDetails: bool,
  bFailOnDecodeBodyErrors: bool,
  xPrefix = [],
):
  sbData = oMessage.sbBody;
  o0Trailers = None;
  if oMessage.fbHasChunkedEncodingHeader():
    oChunkedData = oMessage.foChunkedDecodeData(sbData);
    sbData = oChunkedData.sbData;
    o0Trailers = oChunkedData.oTrailers;
  if bFailOnDecodeBodyErrors:
    sbData = oMessage.fsbDecompressData(sbData);
  else:
    asbCompressionTypes = oMessage.fasbGetCompressionTypes();
    (sbData, asbActualCompressionTypes) = oMessage.ftxDecompressDataAndGetActualCompressionTypes(sbData);
    if asbCompressionTypes != asbActualCompressionTypes:
      if asbActualCompressionTypes:
        oConsole.fOutput(
          xPrefix,
          [COLOR_REQUEST_RESPONSE_BOX, "│ "] if bShowDetails else [], 
          COLOR_WARNING, CHAR_WARNING, " NOTE",
          COLOR_NORMAL, ": The body was compressed using ",
          faxListOutput(
            asData = [str(sbCompressionType, "ascii", "strict") for sbCompressionType in asbActualCompressionTypes],
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
  sData = oMessage.fsCharacterDecodeData(sbData);
  if len(sData) == 0:
    if bShowDetails:
      oConsole.fOutput(
        xPrefix,
        COLOR_EOF, CHAR_EOF,
      );
    return;
  sLine = "";
  asEOL = [];
  uIndex = 0;
  bMessageHasNoTrailers = o0Trailers is None or o0Trailers.uNumberOfNamedValues == 0;
  while 1:
    bIsLastChar = uIndex == len(sData) - 1;
    sChar = sData[uIndex];
    uIndex += 1;
    if sChar == "\r":
      if bIsLastChar or sData[uIndex] != "\n":
        asEOL = [COLOR_CR, CHAR_CR];
      else:
        asEOL = [COLOR_CRLF, CHAR_CRLF];
        uIndex += 1;
    elif sChar == "\n":
      asEOL = [COLOR_LF, CHAR_LF];
    else:
      sLine += sChar;
    bEOF = uIndex == len(sData) and bMessageHasNoTrailers;
    if asEOL or bEOF:
      oConsole.fOutput(
        xPrefix,
        COLOR_DATA, sLine,
        asEOL if bShowDetails else [],
        [COLOR_EOF, CHAR_EOF] if bEOF and bShowDetails else [],
      );
      if bEOF:
        break;
      sLine = "";
      asEOL = [];
  if o0Trailers:
    fOutputHTTPMessageHeadersOrTrailers(
      oHeadersOrTrailers = o0Trailers,
      bShowDetails = bShowDetails,
      bShowEOF = True,
      xPrefix = xPrefix,
    );