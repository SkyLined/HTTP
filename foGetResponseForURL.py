import sys;

from mNotProvided import fbIsProvided;

from foConsoleLoader import foConsoleLoader;
from foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;
from mColorsAndChars import *;
from mExitCodes import \
    guExitCodeRequestDataInFileIsNotUTF8;
oConsole = foConsoleLoader();

def foGetResponseForURL(
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
  bConcatinateDownload,
  bShowProgress,
):
  if d0Form_sValue_by_sName is not None and not fbIsProvided(sbzMethod):
    sbzMethod = b"POST";
  # Construct the HTTP request
  try:
    oRequest = oHTTPClient.foGetRequestForURL(
      oURL = oURL,
      sbzVersion = sbzHTTPVersion,
      sbzMethod = sbzMethod,
      sb0Body = sb0RequestBody,
      s0Data = s0RequestData,
    );
  except oHTTPClient.cHTTPInvalidEncodedDataException as oException:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " The provided utf-8 encoded data cannot be encoded: ",
      COLOR_INFO, oException.sMessage,
      COLOR_NORMAL, ".",
    );
    sys.exit(guExitCodeRequestDataInFileIsNotUTF8);

  # Apply headers provided through arguments to request
  for (sbName, sbValue) in dsbAdditionalOrRemovedHeaders.items():
    if sbValue is None:
      oRequest.oHeaders.fbRemoveHeadersForName(sbName);
    else:
      oRequest.oHeaders.fbReplaceHeadersForNameAndValue(sbName, sbValue);
  if d0Form_sValue_by_sName:
    oRequest.oHeaders.fbReplaceHeadersForNameAndValue(b"Content-Type", b"application/x-www-form-urlencoded");
    for (sName, sValue) in d0Form_sValue_by_sName.items():
      oRequest.fSetFormValue(sName, sValue);
  
  return foGetResponseForRequestAndURL(
    oHTTPClient = oHTTPClient,
    oRequest = oRequest,
    oURL = oURL,
    u0MaxRedirects = u0MaxRedirects,
    bDownloadToFile = bDownloadToFile,
    bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
    bSaveToFile = bSaveToFile,
    s0TargetFilePath = s0TargetFilePath,
    bConcatinateDownload = bConcatinateDownload,
    bShowProgress = bShowProgress,
  );
