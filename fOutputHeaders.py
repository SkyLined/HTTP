from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputHeaders(oHeaders, xPrefix = []):
  for oHTTPHeader in oHeaders.faoGetHeaders():
    asbValueLines = oHTTPHeader.asbValueLines;
    oConsole.fOutput(
      xPrefix,
      COLOR_HEADER_NAME, fsCP437FromBytesString(oHTTPHeader.sbName),
      COLOR_NORMAL, ": ",
      COLOR_HEADER_VALUE, fsCP437FromBytesString(asbValueLines[0]),
      COLOR_CRLF, CHAR_CRLF,
    );
    for sbValueLine in asbValueLines[1:]:
      oConsole.fOutput(
        xPrefix,
        COLOR_HEADER_VALUE, fsCP437FromBytesString(sbValueLine),
      );
