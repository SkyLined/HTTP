from mHTTPProtocol import iMessage;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_BODY,
  COLOR_CR, CHAR_CR,
  COLOR_CRLF, CHAR_CRLF,
  COLOR_EOF, CHAR_EOF,
  COLOR_LF, CHAR_LF,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromByte;
oConsole = foConsoleLoader();

def fOutputHTTPMessageBodyAsIs(
  oMessage: iMessage,
  *,
  bShowDetails: bool,
  bForceHexOutput = False,
  uHexOutputCharsPerLine = 16,
  xPrefix = [],
):
  sbBody = oMessage.sbBody;
  if len(sbBody) == 0:
    if bShowDetails:
      oConsole.fOutput(
        xPrefix,
        COLOR_EOF, CHAR_EOF,
      );
    return;
  if bForceHexOutput or any(uByte < 0x20 and uByte not in b"\r\n\t" for uByte in sbBody):
    # None ASCII bytes: dump as hex.
    asBytesOutput = [];
    sCharsOutput = "";
    uOffset = 0;
    while uOffset < len(sbBody):
      # byte
      asBytesOutput.append("%02X" % sbBody[uOffset]);
      # char
      sCharsOutput += fsCP437FromByte(sbBody[uOffset]);
      uOffset += 1;
      bEOL = len(sCharsOutput) == uHexOutputCharsPerLine;
      bEOF = uOffset == len(sbBody);
      if bEOL or bEOF:
        oConsole.fOutput(
          xPrefix,
          COLOR_BODY, " ".join(asBytesOutput).ljust(3 * uHexOutputCharsPerLine - 1),
          COLOR_NORMAL, " ┊ ",
          COLOR_BODY, sCharsOutput,
          [COLOR_EOF, CHAR_EOF] if bEOF and bShowDetails else [],
        );
        asBytesOutput = [];
        sCharsOutput = "";
  else:
    uCR = b"\r"[0];
    uLF = b"\n"[0];
    sLine = "";
    asEOL = [];
    uIndex = 0;
    while 1:
      bIsLastChar = uIndex == len(sbBody) - 1;
      uByte = sbBody[uIndex];
      uIndex += 1;
      if uByte == uCR:
        if bIsLastChar or sbBody[uIndex] != uLF:
          asEOL = [COLOR_CR, CHAR_CR];
        else:
          asEOL = [COLOR_CRLF, CHAR_CRLF];
          uIndex += 1;
      elif uByte == uLF:
        asEOL = [COLOR_LF, CHAR_LF];
      else:
        sLine += fsCP437FromByte(uByte);
      bEOF = uIndex == len(sbBody);
      if asEOL or bEOF:
        oConsole.fOutput(
          xPrefix,
          COLOR_BODY, sLine,
          asEOL if bShowDetails else [],
          [COLOR_EOF, CHAR_EOF] if bEOF and bShowDetails else [],
        );
        if bEOF:
          return;
        sLine = "";
        asEOL = [];