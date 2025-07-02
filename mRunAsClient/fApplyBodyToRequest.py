import sys;

from mHTTPProtocol import (
  cDataCannotBeEncodedWithCharsetException,
  cInvalidCharsetValueException,
  cRequest,
  cUnhandledCharsetValueException,
  cUnhandledCompressionTypeValueException,
);

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mExitCodes import (
  guExitCodeInvalidRequestData,
  guExitCodeUnhandledCharacterEncoding,
  guExitCodeUnhandledCompressionType,
);
oConsole = foConsoleLoader();

def fApplyBodyToRequest(*,
  oRequest: cRequest,
  sxBody: bytes | str,
  bCompress: bool,
  bApplyChunkedEncoding: bool,
  bSetContentLengthHeader: bool,
):
  if isinstance(sxBody, str):
    try:
      sbBody = oRequest.fsbCharacterEncodeData(
        sData = sxBody,
      );
    except cDataCannotBeEncodedWithCharsetException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The provided data cannot be encoded: ",
        COLOR_INFO, oException.sMessage,
        COLOR_NORMAL, ".",
      );
      sys.exit(guExitCodeInvalidRequestData);
    except cInvalidCharsetValueException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The provided charset value is invalid: ",
        COLOR_INFO, oException.sMessage,
        COLOR_NORMAL, ".",
      );
      sys.exit(guExitCodeUnhandledCharacterEncoding);
    except cUnhandledCharsetValueException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The provided charset value is not handled: ",
        COLOR_INFO, oException.sMessage,
        COLOR_NORMAL, ".",
      );
      sys.exit(guExitCodeUnhandledCharacterEncoding);
  elif sxBody is not None:
    sbBody = sxBody; # assume bytes
  if bCompressBody:
    try:
      sbBody = oRequest.fsbCompressData(
        sbData = sbBody,
      );
    except cUnhandledCompressionTypeValueException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The provided compression type is not handled: ",
        COLOR_INFO, oException.sMessage,
        COLOR_NORMAL, ".",
      );
      sys.exit(guExitCodeUnhandledCompressionType);
  if bApplyChunkedEncoding:
    sbBody = oRequest.fsbOptionallyChunkedEncodeData(
      sbData = sbBody,
    );
  oRequest.fSetBody(
    sbData = sbBody,
    bSetContentLengthHeader = bSetContentLengthHeader,
  );
