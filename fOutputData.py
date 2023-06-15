from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import \
  COLOR_DATA, \
  COLOR_CR, CHAR_CR, \
  COLOR_CRLF, CHAR_CRLF, \
  COLOR_EOF, CHAR_EOF, \
  COLOR_LF, CHAR_LF, \
  COLOR_NORMAL;
from mCP437 import fsCP437FromByte;
oConsole = foConsoleLoader();

def fOutputData(
  sData,
  *,
  bShowDetails = None,
  bOutputEOF = None,
  xPrefix = [],
):
  assert bShowDetails is not None, \
      "You must specify a value for bShowDetails.";
  assert bOutputEOF is not None, \
      "You must specify a value for bOutputEOF.";
  sLine = "";
  asEOL = [];
  uIndex = 0;
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
    bEOF = uIndex == len(sData);
    if asEOL or bEOF:
      oConsole.fOutput(
        xPrefix,
        COLOR_DATA, sLine,
        asEOL if bShowDetails else [],
        [COLOR_EOF, CHAR_EOF] if bEOF and bShowDetails and bOutputEOF else [],
      );
      if bEOF:
        return;
      sLine = "";
      asEOL = [];