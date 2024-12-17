import sys;

from mHTTPProtocol import (
  cHTTPInvalidEncodedDataException,
);
from mNotProvided import fbIsProvided;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mExitCodes import guExitCodeRequestDataInFileIsNotUTF8;
oConsole = foConsoleLoader();

from .fApplyHeaderSettingsToRequest import fApplyHeaderSettingsToRequest;
from .foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;

def foGetResponseForURL(
  *, 
  oHTTPClient,
  oURL,
  sbzSetHTTPVersion,
  sbzSetMethod,
  sb0SetHTTPRequestBody,
  s0SetHTTPRequestData,
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
  bConcatenateDownload,
  bShowProgress,
):
  if not fbIsProvided(sbzSetMethod):
    if d0SetForm_sValue_by_sName is not None or d0SetJSON_sValue_by_sName is not None:
      sbzSetMethod = b"POST";
  # Construct the HTTP request
  try:
    oRequest = oHTTPClient.foGetRequestForURL(
      oURL = oURL,
      sbzVersion = sbzSetHTTPVersion,
      sbzMethod = sbzSetMethod,
      sb0Body = sb0SetHTTPRequestBody,
      s0Data = s0SetHTTPRequestData,
      bAddContentLengthHeader = True, # This header can be removed/modified later through the header arguments
    );
  except cHTTPInvalidEncodedDataException as oException:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " The provided utf-8 encoded data cannot be encoded: ",
      COLOR_INFO, oException.sMessage,
      COLOR_NORMAL, ".",
    );
    sys.exit(guExitCodeRequestDataInFileIsNotUTF8);

  # Applying form and JSON values sets the Content-Type header. This must be
  # done before we call `fApplyHeaderSettingsToRequest` so the user can
  # overwrite or remove this header later.
  if d0SetForm_sValue_by_sName:
    for (sName, sValue) in d0SetForm_sValue_by_sName.items():
      oRequest.fSetFormValue(sName, sValue);
  if d0SetJSON_sValue_by_sName:
    for (sName, sValue) in d0SetJSON_sValue_by_sName.items():
      oRequest.fSetJSONValue(sName, sValue);
  # Apply headers provided through arguments to request
  fApplyHeaderSettingsToRequest(
    asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
    dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
    atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
    oRequest = oRequest,
  );
  
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
