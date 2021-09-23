from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromByte;

def fOutputBody(sxBody, bOutputEOF):
  if isinstance(sxBody, str):
    xCR = "\r";
    xLF = "\n";
    xBodyColor = COLOR_BODY_DECODED;
    fsChar = lambda sChar: sChar;
  else:
    xCR = ord("\r");
    xLF = ord("\n");
    xBodyColor = COLOR_BODY;
    fsChar = lambda uByte: fsCP437FromByte(uByte);
  
  sLine = "";
  a0sEOL = [];
  uIndex = 0;
  while 1:
    bIsLastChar = uIndex == len(sxBody) - 1;
    xCharOrByte = sxBody[uIndex];
    uIndex += 1;
    if xCharOrByte == xCR:
      if bIsLastChar or sxBody[uIndex] != xLF:
        a0sEOL = [COLOR_CR, CHAR_CR];
      else:
        a0sEOL = [COLOR_CRLF, CHAR_CRLF];
        uIndex += 1;
    elif xCharOrByte == xLF:
      a0sEOL = [COLOR_LF, CHAR_LF];
    else:
      sLine += fsChar(xCharOrByte);
    bEOF = uIndex == len(sxBody);
    if a0sEOL or bEOF:
      oConsole.fOutput(
        COLOR_REQUEST_RESPONSE_BOX, "│ ", 
        xBodyColor, sLine,
        a0sEOL if a0sEOL else [],
        [COLOR_EOF, CHAR_EOF] if bEOF else [],
      );
      if bEOF:
        return;
      sLine = "";
      a0sEOL = None;