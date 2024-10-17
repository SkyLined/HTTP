import sys;

from mNotProvided import fbIsProvided;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mExitCodes import guExitCodeRequestDataInFileIsNotUTF8;
oConsole = foConsoleLoader();

from .foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;

def foGetResponseForURL(
  *, 
  oHTTPClient,
  oURL,
  sbzSetHTTPVersion,
  sbzSetMethod,
  sb0SetHTTPRequestBody,
  s0SetHTTPRequestData,
  dsbAddOrRemoveHeaders,
  d0SetForm_sValue_by_sName,
  u0MaxRedirects,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bSaveHTTPResponsesToFiles,
  o0DownloadToFileSystemItem,
  o0SaveHTTPResponsesToFileSystemItem,
  bConcatenateDownload,
  bShowProgress,
):
  if d0SetForm_sValue_by_sName is not None and not fbIsProvided(sbzSetMethod):
    sbzSetMethod = b"POST";
  # Construct the HTTP request
  try:
    oRequest = oHTTPClient.foGetRequestForURL(
      oURL = oURL,
      sbzVersion = sbzSetHTTPVersion,
      sbzMethod = sbzSetMethod,
      sb0Body = sb0SetHTTPRequestBody,
      s0Data = s0SetHTTPRequestData,
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
  for (sbName, sbValue) in dsbAddOrRemoveHeaders.items():
    if sbValue is None:
      oRequest.oHeaders.fbRemoveHeadersForName(sbName);
    else:
      oRequest.oHeaders.fbReplaceHeadersForNameAndValue(sbName, sbValue);
  if d0SetForm_sValue_by_sName:
    oRequest.oHeaders.fbReplaceHeadersForNameAndValue(b"Content-Type", b"application/x-www-form-urlencoded");
    for (sName, sValue) in d0SetForm_sValue_by_sName.items():
      oRequest.fSetFormValue(sName, sValue);
  
  return foGetResponseForRequestAndURL(
    oHTTPClient = oHTTPClient,
    oRequest = oRequest,
    oURL = oURL,
    u0MaxRedirects = u0MaxRedirects,
    bDownloadToFile = bDownloadToFile,
    bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
    bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
    o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
    o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
    bConcatenateDownload = bConcatenateDownload,
    bShowProgress = bShowProgress,
  );
