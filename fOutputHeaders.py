from mConsole import oConsole;

import mColors;
import mSpecialChars;
from mCP437 import fsCP437FromBytesString;

def fOutputHeaders(oHeaders):
  for oHTTPHeader in oHeaders.faoGetHeaders():
    asbValueLines = oHTTPHeader.asbValueLines;
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_HEADER_NAME, fsCP437FromBytesString(oHTTPHeader.sbName),
      mColors.NORMAL, ": ",
      mColors.HTTP_HEADER_VALUE, fsCP437FromBytesString(asbValueLines[0]),
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
    );
    for sbValueLine in asbValueLines[1:]:
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        mColors.HTTP_HEADER_VALUE, fsCP437FromBytesString(sbValueLine),
      );
