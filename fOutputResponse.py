from oConsole import oConsole;

from fOutputBody import fOutputBody;
from fOutputHeaders import fOutputHeaders;
import mColors;
import mSpecialChars;

def fOutputResponse(oResponse, bDecodeBody, bShowDetails):
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_TOPLEFT, mSpecialChars.BOX_OUTPUT_HEADER_PREFIX,
    mColors.HTTP_REQUEST_RESPONSE_BOX_HEADER, " Response ",
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_HEADER_POSTFIX,
    sPadding = mSpecialChars.BOX_OUTPUT_TOP
  );
  ### OUTPUT RESPONSE ####################################################
  # Output response status line
  if 100 <= oResponse.uStatusCode < 200: 
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_1xx;
  elif 200 <= oResponse.uStatusCode < 300: 
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_2xx;
  elif 300 <= oResponse.uStatusCode < 400: 
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_3xx;
  elif 400 <= oResponse.uStatusCode < 500: 
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_4xx;
  elif 500 <= oResponse.uStatusCode < 600: 
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_5xx;
  else:
    xStatusLineColor = mColors.HTTP_RESPONSE_STATUS_LINE_INVALID;
  oConsole.fOutput(
    mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
    xStatusLineColor, oResponse.fsGetStatusLine(),
    mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
  );
  if bShowDetails:
    fOutputHeaders(oResponse.oHeaders);
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
      *([mColors.HTTP_EOF, mSpecialChars.HTTP_EOF] if not oResponse.sBody and not oResponse.o0AdditionalHeaders else [])
    );
  # Output response body if any
  if oResponse.sBody:
    if bDecodeBody:
      s0Body = oResponse.s0Data;
      xBodyColor = mColors.HTTP_BODY_DECODED;
    else:
      s0Body = oResponse.sBody if oResponse.sBody else None;
      xBodyColor = mColors.HTTP_BODY;
    if s0Body is not None:
      fOutputBody(xBodyColor, s0Body, bOutputEOF = not oResponse.o0AdditionalHeaders);
  if bShowDetails and oResponse.o0AdditionalHeaders:
    # Output response additional headers
    fOutputHeaders(oResponse.o0AdditionalHeaders);
    oConsole.fOutput(
      mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_LEFT, 
      mColors.HTTP_CRLF, mSpecialChars.HTTP_CRLF,
      mColors.HTTP_EOF, mSpecialChars.HTTP_EOF,
    );
  oConsole.fOutput(mColors.HTTP_REQUEST_RESPONSE_BOX, mSpecialChars.BOX_OUTPUT_BOTTOMLEFT, sPadding = mSpecialChars.BOX_OUTPUT_BOTTOM);
