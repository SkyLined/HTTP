from mConsole import oConsole;

from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
from mCP437 import fsCP437FromBytesString;
import mColors;
import mSpecialChars;

def fOutputRequest(oRequest, bDecodeBody, bShowDetails):
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_TOPLEFT, mSpecialChars.BOX_OUTPUT_HEADER_PREFIX,
    mColors.HTTP_REQUEST_RESPONSE_BOX_HEADER, " Request ",
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_HEADER_POSTFIX,
    sPadding = mSpecialChars.BOX_OUTPUT_TOP
  );
  # Output request status line
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
    mColors.HTTP_REQUEST_STATUS_LINE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()),
    mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
  );
  if bShowDetails:
    # Output request headers
    fOutputHeaders(oRequest.oHeaders);
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
      *([mColors.HTTP_EOF, mSpecialChars.HTTP_EOF] if not oRequest.sb0Body is not None else [])
    );
    if oRequest.sb0Body:
      if bDecodeBody:
        # Output decoded request body if any
        fOutputBody(oRequest.s0Data, bOutputEOF = not oRequest.o0AdditionalHeaders);
      else:
        # Output request body if any
        fOutputBody(oRequest.sb0Body, bOutputEOF = not oRequest.o0AdditionalHeaders);
    if oRequest.o0AdditionalHeaders:
      # Output response additional headers
      fOutputHeaders(oRequest.o0AdditionalHeaders);
      oConsole.fOutput(
        mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
        mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
        mColors.HTTP_EOF, mSpecialChars.HTTP_EOF,
      );
  oConsole.fOutput(mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_BOTTOMLEFT, sPadding = mSpecialChars.BOX_OUTPUT_BOTTOM);
