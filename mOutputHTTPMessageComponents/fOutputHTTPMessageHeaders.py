from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_CRLF, CHAR_CRLF,
  COLOR_HEADER_NAME,
  COLOR_HEADER_VALUE,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;
from mOutputHelpers import faxGetDecodedValuesOutput;
oConsole = foConsoleLoader();

def fOutputHTTPMessageHeaders(oHeaders, bShowDetails, xPrefix = []):
  for oHTTPHeader in oHeaders.faoGetHeaders():
    asbValueLines = oHTTPHeader.asbValueLines;
    oConsole.fOutput(
      xPrefix,
      COLOR_HEADER_NAME, fsCP437FromBytesString(oHTTPHeader.sbName),
      COLOR_NORMAL, ":",
      COLOR_HEADER_VALUE, fsCP437FromBytesString(asbValueLines[0]),
      [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
    );
    for sbValueLine in asbValueLines[1:]:
      oConsole.fOutput(
        xPrefix,
        COLOR_HEADER_VALUE, fsCP437FromBytesString(sbValueLine),
        [COLOR_CRLF, CHAR_CRLF] if bShowDetails else [],
      );
    sbValue = b" ".join(asbValueLines);
    for xDecodedValueOutput in faxGetDecodedValuesOutput(sbValue):
      oConsole.fOutput("  ", xDecodedValueOutput);

