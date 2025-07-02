import re, sys;

from mHTTPProtocol import cURL;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_HILITE,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_OK, CHAR_OK,
);
from mExitCodes import guExitCodeBadArgument;
oConsole = foConsoleLoader();

from .foGetResponseForURL import foGetResponseForURL;

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

def fProcessSegmentedVideo(
  *,
  oHTTPClient,
  oURL,
  sbzHTTPVersion,
  sbzMethod,
  sx0Body,
  bAddContentLengthHeaderForBody,
  bApplyChunkedEncodingToBody,
  bCompressBody,
  asbRemoveHeadersForLowerNames,
  dtsbReplaceHeaderNameAndValue_by_sLowerName,
  atsbAddHeadersNameAndValue,
  d0SetForm_sValue_by_sName,
  d0SetJSON_sValue_by_sName,
  u0MaxRedirects,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bSaveHTTPResponsesToFiles,
  o0DownloadToFileSystemItem,
  o0SaveHTTPResponsesToFileSystemItem,
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
      sx0Body = sx0Body,
      bAddContentLengthHeaderForBody = bAddContentLengthHeaderForBody,
      bApplyChunkedEncodingToBody = bApplyChunkedEncodingToBody,
      bCompressBody = bCompressBody,
      asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
      dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
      atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
      d0SetForm_sValue_by_sName = d0SetForm_sValue_by_sName,
      d0SetJSON_sValue_by_sName = d0SetJSON_sValue_by_sName,
      u0MaxRedirects = u0MaxRedirects,
      bDownloadToFile = bDownloadToFile,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
      o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
      o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
      bConcatenateDownload = uIndex != uStartIndex,
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
