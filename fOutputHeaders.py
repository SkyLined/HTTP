from oConsole import oConsole;

import mColors;
import mSpecialChars;

def fOutputHeaders(oHeaders):
  for oHTTPHeader in oHeaders.faoGetHeaders():
    asValueLines = oHTTPHeader.asValueLines;
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_HEADER_NAME, oHTTPHeader.sName,
      mColors.NORMAL, ": ",
      mColors.HTTP_HEADER_VALUE, asValueLines[0],
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
    );
    for sValueLine in asValueLines[1:]:
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        mColors.HTTP_HEADER_VALUE, sValueLine,
      );
