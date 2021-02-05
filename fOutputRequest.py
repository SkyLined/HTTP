from oConsole import oConsole;

from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
import mColors;
import mSpecialChars;

def fOutputRequest(oRequest, bShowDetails):
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_TOPLEFT, mSpecialChars.BOX_OUTPUT_HEADER_PREFIX,
    mColors.HTTP_REQUEST_RESPONSE_BOX_HEADER, " Request ",
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_HEADER_POSTFIX,
    sPadding = mSpecialChars.BOX_OUTPUT_TOP
  );
  # Output request status line
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
    mColors.HTTP_REQUEST_STATUS_LINE, oRequest.fsGetStatusLine(),
    mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
  );
  if bShowDetails:
    # Output request headers
    fOutputHeaders(oRequest.oHeaders);
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
      *([mColors.HTTP_EOF, mSpecialChars.HTTP_EOF] if not oRequest.sBody else [])
    );
    if oRequest.sBody:
      # Output request body if any
      fOutputBody(mColors.HTTP_BODY, oRequest.sBody, bOutputEOF = not oRequest.o0AdditionalHeaders);
    if oRequest.o0AdditionalHeaders:
      # Output response additional headers
      fOutputHeaders(oRequest.o0AdditionalHeaders);
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
        mColors.HTTP_EOF, mSpecialChars.HTTP_EOF,
      );
  oConsole.fOutput(mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_BOTTOMLEFT, sPadding = mSpecialChars.BOX_OUTPUT_BOTTOM);
