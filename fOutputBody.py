from mConsole import oConsole;

from mCP437 import fsCP437FromByte;
import mColors;
import mSpecialChars;

def fOutputBody(sxBody, bOutputEOF):
  if isinstance(sxBody, str):
    xCR = "\r";
    xLF = "\n";
    xBodyColor = mColors.HTTP_BODY_DECODED;
    fsChar = lambda sChar: sChar;
  else:
    xCR = ord("\r");
    xLF = ord("\n");
    xBodyColor = mColors.HTTP_BODY;
    fsChar = lambda uByte: fsCP437FromByte(uByte);
  
  sLine = "";
  s0CRLF = "";
  uIndex = 0;
  while 1:
    bIsLastChar = uIndex == len(sxBody) - 1;
    xCharOrByte = sxBody[uIndex];
    uIndex += 1;
    if xCharOrByte == xCR:
      if bIsLastChar or sxBody[uIndex] != xLF:
        s0CRLF = mSpecialChars.HTTP_CR;
      else:
        s0CRLF = mSpecialChars.HTTP_CRLF;
        uIndex += 1;
    elif xCharOrByte == xLF:
      s0CRLF = mSpecialChars.HTTP_LF;
    else:
      sLine += fsChar(xCharOrByte);
    bEOF = uIndex == len(sxBody);
    if s0CRLF or bEOF:
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        xBodyColor, sLine,
        [mColors.HTTP_CRLF, s0CRLF] if s0CRLF else [],
        [mColors.HTTP_EOF, mSpecialChars.HTTP_EOF] if bEOF else [],
      );
      if bEOF:
        return;
      sLine = "";
      s0CRLF = None;