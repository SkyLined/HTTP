from oConsole import oConsole;

import mColors;
import mSpecialChars;

def fOutputBody(xBodyColor, sBody, bOutputEOF):
  sLine = "";
  sCRLF = "";
  uIndex = 0;
  while 1:
    bIsLastChar = uIndex == len(sBody) - 1;
    sChar = sBody[uIndex];
    uIndex += 1;
    if sChar == "\r":
      if bIsLastChar or sBody[uIndex] != "\n":
        sCRLF = mSpecialChars.HTTP_CR;
      else:
        sCRLF = mSpecialChars.HTTP_CRLF;
        uIndex += 1;
    elif sChar == "\n":
      sCRLF = mSpecialChars.HTTP_LF;
    else:
      sLine += sChar;
    bEOF = uIndex == len(sBody);
    if sCRLF or bEOF:
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        xBodyColor, sLine,
        [mColors.HTTP_CRLF, sCRLF] if sCRLF else [],
        [mColors.HTTP_EOF, mSpecialChars.HTTP_EOF] if bEOF else [],
      );
      if bEOF:
        return;
      sLine = "";
      sCRLF = "";