import re, sys;

from mHTTPProtocol import cURL;

from foConsoleLoader import foConsoleLoader;
from foGetResponseForURL import foGetResponseForURL;
from mColorsAndChars import \
  COLOR_ERROR, CHAR_ERROR, \
  COLOR_HILITE, \
  COLOR_INFO, \
  COLOR_NORMAL, \
  COLOR_OK, CHAR_OK;
from mExitCodes import \
    guExitCodeBadArgument;
oConsole = foConsoleLoader();

garbSegmentedVideos = [re.compile(sb) for sb in [
  (
    rb"("
      rb".*?/"
      rb"(?:\w+\-)+?"
    rb")("
      rb"\d+"
    rb")("
      rb"(?:\-\w+)*"
      rb"\.ts"
      rb"(?:\?.*)?"
    rb")"
  ), (
    rb"("
      rb".*?/"
      rb"(?:\w+\-)+?"
      rb"(?:\w*?)"
    rb")("
      rb"\d+"
    rb")("
      rb"(?:\-\w+)*"
      rb"\.ts"
      rb"(?:\?.*)?"
    rb")"
  )
]];

def fHandleSegmentedVideo(
  *,
  oHTTPClient,
  oURL,
  sbzHTTPVersion,
  sbzMethod,
  sb0RequestBody,
  s0RequestData,
  dsbAdditionalOrRemovedHeaders,
  d0Form_sValue_by_sName,
  u0MaxRedirects,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bSaveToFile,
  s0TargetFilePath,
  bShowProgress,
):
  for rbSegmentedVideo in garbSegmentedVideos:
    obURLSegmentMatch = rbSegmentedVideo.match(oURL.sbAbsolute);
    if obURLSegmentMatch:
      break;
  else:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Could not identify segmentation from URL \"",
      COLOR_INFO, oURL.sbAbsolute,
      COLOR_NORMAL, "\"",
    );
    sys.exit(guExitCodeBadArgument);
  sbURLSegmentHeader, sbStartIndex, sbURLSegmentFooter = obURLSegmentMatch.groups();
  uStartIndex = int(sbStartIndex);
  if bShowProgress:
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Segmented URL: \"",
      COLOR_INFO, str(sbURLSegmentHeader, "ascii", "replace"),
      COLOR_HILITE, "*INDEX*",
      COLOR_INFO, str(sbURLSegmentFooter, "ascii", "replace"),
      COLOR_NORMAL, "\".",
    );
    oConsole.fOutput(
      COLOR_NORMAL, "  Index will start at ",
      COLOR_HILITE, str(uStartIndex),
      COLOR_NORMAL, ".",
    );
  uIndex = uStartIndex;
  while 1:
    oURL = cURL.foFromBytesString(b"%s%d%s" % (sbURLSegmentHeader, uIndex, sbURLSegmentFooter));
    oResponse = foGetResponseForURL(
      oHTTPClient = oHTTPClient,
      oURL = oURL,
      sbzHTTPVersion = sbzHTTPVersion,
      sbzMethod = sbzMethod,
      sb0RequestBody = sb0RequestBody,
      s0RequestData = s0RequestData,
      dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
      d0Form_sValue_by_sName = d0Form_sValue_by_sName,
      u0MaxRedirects = u0MaxRedirects,
      bDownloadToFile = bDownloadToFile,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bSaveToFile = bSaveToFile,
      s0TargetFilePath = s0TargetFilePath,
      bConcatinateDownload = uIndex != uStartIndex,
      bShowProgress = bShowProgress,
    );
    if oResponse.uStatusCode != 200:
      break;
    uIndex += 1;
  if bShowProgress:
    oConsole.fOutput(
      "      ",
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Found ",
      COLOR_INFO, str(uIndex - uStartIndex),
      COLOR_NORMAL, " segments.",
    );
