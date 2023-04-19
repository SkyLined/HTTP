from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromByte;
oConsole = foConsoleLoader();

def fOutputBody(sxBody, bNeedsDecoding, bShowDetails, bOutputEOF, xPrefix = []):
  if isinstance(sxBody, str):
    xCR = "\r";
    xLF = "\n";
    fsChar = lambda sChar: sChar;
  else:
    xCR = ord("\r");
    xLF = ord("\n");
    fsChar = lambda uByte: fsCP437FromByte(uByte);
  xBodyColor = COLOR_BODY if bNeedsDecoding else COLOR_BODY_DECODED;
  
  sLine = "";
  asEOL = [];
  uIndex = 0;
  while 1:
    bIsLastChar = uIndex == len(sxBody) - 1;
    xCharOrByte = sxBody[uIndex];
    uIndex += 1;
    if xCharOrByte == xCR:
      if bIsLastChar or sxBody[uIndex] != xLF:
        asEOL = [COLOR_CR, CHAR_CR];
      else:
        asEOL = [COLOR_CRLF, CHAR_CRLF];
        uIndex += 1;
    elif xCharOrByte == xLF:
      asEOL = [COLOR_LF, CHAR_LF];
    else:
      sLine += fsChar(xCharOrByte);
    bEOF = uIndex == len(sxBody);
    if asEOL or bEOF:
      oConsole.fOutput(
        xPrefix,
        xBodyColor, sLine,
        asEOL if bShowDetails else [],
        [COLOR_EOF, CHAR_EOF] if bEOF and bShowDetails and bOutputEOF else [],
      );
      if bEOF:
        return;
      sLine = "";
      asEOL = [];