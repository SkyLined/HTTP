import sys;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import \
  COLOR_ERROR, CHAR_ERROR, \
  COLOR_INFO, \
  COLOR_NORMAL, \
  COLOR_OK, CHAR_OK, \
  COLOR_WARNING, CHAR_WARNING;
oConsole = foConsoleLoader();

from faoGetURLsFromM3U import faoGetURLsFromM3U;
from foGetResponseForURL import foGetResponseForURL;
from mExitCodes import \
    guExitCodeNoValidResponseReceived;

def fHandleM3U(
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
  bFixDecodeBodyErrors,
  bSaveToFile,
  s0TargetFilePath,
  bShowProgress,
  bSegmentedM3U,
):
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
    bDownloadToFile = False,
    bFixDecodeBodyErrors = bFixDecodeBodyErrors,
    bSaveToFile = False,
    s0TargetFilePath = None,
    bConcatinateDownload = False,
    bShowProgress = bShowProgress,
  );
  if oResponse.uStatusCode != 200:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Cannot download M3U file.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  s0M3UContents = oResponse.fs0GetData();
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
  if bSegmentedM3U and s0TargetFilePath is None:
    asPathSegments = oURL.asURLDecodedPath;
    if asPathSegments:
      s0TargetFilePath = asPathSegments[-1] + ".mp4";
    else:
      s0TargetFilePath = "video.mp4";
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
      sb0RequestBody = sb0RequestBody,
      s0RequestData = s0RequestData,
      dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
      d0Form_sValue_by_sName = d0Form_sValue_by_sName,
      u0MaxRedirects = u0MaxRedirects,
      bDownloadToFile = bDownloadToFile,
      bFixDecodeBodyErrors = bFixDecodeBodyErrors,
      bSaveToFile = bSaveToFile,
      s0TargetFilePath = s0TargetFilePath,
      bConcatinateDownload = uProcessedURLs > 0 if bSegmentedM3U else False,
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
