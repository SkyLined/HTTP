from mHTTPProtocol import iMessage;
from .fOutputHTTPMessageBodyAsData import fOutputHTTPMessageBodyAsData;
from .fOutputHTTPMessageBodyAsIs import fOutputHTTPMessageBodyAsIs;

from mColorsAndChars import (
  COLOR_REQUEST_RESPONSE_BOX,
);

def fOutputHTTPMessageBody(
  oMessage: iMessage,
  *,
  bDecodeBody: bool,
  bFailOnDecodeBodyErrors: bool,
  bShowDetails: bool,
  bForceHexOutput: bool = False,
  uHexOutputCharsPerLine: int = 16,
  xPrefix: list = [],
):
  if bDecodeBody:
    fOutputHTTPMessageBodyAsData(
      oMessage,
      bShowDetails = bShowDetails,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      xPrefix = xPrefix,
    );
  else:
    fOutputHTTPMessageBodyAsIs(
      oMessage,
      bShowDetails = bShowDetails,
      bForceHexOutput = bForceHexOutput,
      uHexOutputCharsPerLine = uHexOutputCharsPerLine,
      xPrefix = xPrefix,
    );
