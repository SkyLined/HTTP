from mHTTPProtocol.mHeadersTrailers import iNamedValues;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_CRLF, CHAR_CRLF,
  COLOR_EOF, CHAR_EOF,
  COLOR_HEADER_NAME,
  COLOR_HEADER_VALUE,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
from mOutputHelpers import faxGetDecodedValuesOutput;
oConsole = foConsoleLoader();

def fOutputHTTPMessageHeadersOrTrailers(
  oHeadersOrTrailers: iNamedValues,
  bShowDetails: bool,
  bShowEOF: bool = False,
  xPrefix = [],
):
  aoNamedValues = oHeadersOrTrailers.faoGet();
  for oNamedValue in aoNamedValues:
    asbValueLines = oNamedValue.asbValueLines;
    oConsole.fOutput(
      xPrefix,
      COLOR_HEADER_NAME, fsCP437FromBytesString(oNamedValue.sbName),
      COLOR_NORMAL, ":",
      COLOR_HEADER_VALUE, fsCP437FromBytesString(asbValueLines[0]),
      [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    );
    bEOF = oNamedValue is aoNamedValues[-1];
    for sbValueLine in asbValueLines[1:]:
      oConsole.fOutput(
        xPrefix,
        COLOR_HEADER_VALUE, fsCP437FromBytesString(sbValueLine),
        [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
        [COLOR_EOF, CHAR_EOF] if bShowDetails and bEOF else [],
      );
    sbValue = b" ".join(asbValueLines);
    for xDecodedValueOutput in faxGetDecodedValuesOutput(sbValue):
      oConsole.fOutput("  ", xDecodedValueOutput);

