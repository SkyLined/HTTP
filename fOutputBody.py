from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import \
  COLOR_BODY, \
  COLOR_BODY_DECODED, \
  COLOR_CR, CHAR_CR, \
  COLOR_CRLF, CHAR_CRLF, \
  COLOR_EOF, CHAR_EOF, \
  COLOR_LF, CHAR_LF, \
  COLOR_NORMAL;
from mCP437 import fsCP437FromByte;
oConsole = foConsoleLoader();

def fOutputBody(sxBody, bNeedsDecoding, bShowDetails, bOutputEOF, xPrefix = []):
  if isinstance(sxBody, bytes):
    if any(uByte < 0x20 and uByte not in b"\r\n\t" for uByte in sxBody):
      # None ASCII bytes: dump as hex.
      asBytesOutput = [];
      sCharsOutput = "";
      uOffset = 0;
      while uOffset < len(sxBody):
        # byte
        asBytesOutput.append("%02X" % sxBody[uOffset]);
        # char
        sCharsOutput += fsCP437FromByte(sxBody[uOffset]);
        uOffset += 1;
        if len(sCharsOutput) == 16 or uOffset == len(sxBody):
          oConsole.fOutput(
            xPrefix,
            COLOR_BODY, " ".join(asBytesOutput).ljust(2 * 16 + 15),
            COLOR_NORMAL, "  ",
            COLOR_BODY_DECODED, sCharsOutput
          );
          asBytesOutput = [];
          sCharsOutput = "";
      return;
    xCR = ord("\r");
    xLF = ord("\n");
    fsChar = lambda uByte: fsCP437FromByte(uByte);
  else:
    xCR = "\r";
    xLF = "\n";
    fsChar = lambda sChar: sChar;
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