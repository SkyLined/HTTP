import sys;

from mFileSystemItem import cFileSystemItem;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_OK, CHAR_OK,
  COLOR_WARNING, CHAR_WARNING,
);
from mExitCodes import guExitCodeNoValidResponseReceived;
oConsole = foConsoleLoader();

from .faoGetURLsFromM3U import faoGetURLsFromM3U;
from .foGetResponseForURL import foGetResponseForURL;

def fProcessM3UFile(
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
  bProcessSegmentedM3U,
):
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
    bDownloadToFile = False,
    bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
    bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
    o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
    o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
    bConcatenateDownload = False,
    bShowProgress = bShowProgress,
  );
  if oResponse.uStatusCode != 200:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Cannot download M3U file.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  try:
    s0M3UContents = oResponse.fs0GetData(
      bRemoveCompression = True,
      bTryOtherCompressionTypesOnFailure = True, # best effort
    );
  except cHTTPInvalidEncodedDataException:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Provided URL contains an compressed M3U file that cannot be decompressed.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  if s0M3UContents is None:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Provided URL does not contain an M3U file.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  aoURLs = faoGetURLsFromM3U(s0M3UContents, oURL);
  if not aoURLs:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Provided M3U file URL does not contain any links.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  uProcessedURLs = 0;
  uDownloadedURLs = 0;
  if bProcessSegmentedM3U and o0DownloadToFileSystemItem is None:
    asPathSegments = oURL.asURLDecodedPath;
    if asPathSegments:
      o0DownloadToFileSystemItem = cFileSystemItem(asPathSegments[-1] + ".mp4");
    else:
      o0DownloadToFileSystemItem = cFileSystemItem("video.mp4");
  oConsole.fOutput(
    "      ",
    COLOR_OK, CHAR_OK,
    COLOR_NORMAL, " Provided M3U file URL contains ", COLOR_INFO, str(len(aoURLs)), COLOR_NORMAL, " links.",
  );
  for oURL in aoURLs:
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
      bConcatenateDownload = uProcessedURLs > 0 if bProcessSegmentedM3U else False,
      bShowProgress = bShowProgress,
    );
    if oResponse.uStatusCode != 200 and bDownloadToFile:
      # We are missing a piece of the video, stop.
      break;
    else:
      uDownloadedURLs += 1;
    uProcessedURLs += 1;

  oConsole.fOutput(
    "      ",
    [COLOR_ERROR, CHAR_ERROR] if uDownloadedURLs == 0 else
        [COLOR_WARNING, CHAR_WARNING] if uDownloadedURLs != uProcessedURLs else
        [COLOR_OK, CHAR_OK],
    COLOR_NORMAL, [" Unable to downloaded any "] if uProcessedURLs == 0 else
        [
          " Downloaded all ",
          COLOR_INFO, str(uDownloadedURLs),
        ] if uProcessedURLs == uDownloadedURLs else [
          " Downloaded ",
          COLOR_INFO, str(uDownloadedURLs),
          COLOR_NORMAL, "/",
          COLOR_INFO, str(uProcessedURLs),
        ],
    COLOR_NORMAL, " ",
        ["segments"] if bDownloadToFile else ["files"],
    COLOR_NORMAL, ".",
  );
