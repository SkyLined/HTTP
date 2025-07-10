from mNotProvided import fbIsProvided;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
oConsole = foConsoleLoader();

from .fApplyHeaderSettingsToRequest import fApplyHeaderSettingsToRequest;
from .fApplyBodyToRequest import fApplyBodyToRequest;
from .foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;

def foGetResponseForURL(
  *, 
  oClient,
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
  d0SetJSON_xValue_by_sName,
  u0MaxRedirects,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bSaveHTTPResponsesToFiles,
  o0DownloadToFileSystemItem,
  o0SaveHTTPResponsesToFileSystemItem,
  bConcatenateDownload,
  bShowProgress,
):
  if not fbIsProvided(sbzMethod):
    if d0SetForm_sValue_by_sName is not None or d0SetJSON_xValue_by_sName is not None:
      sbzMethod = b"POST";
  # Construct the HTTP request
  oRequest = oClient.foGetRequestForURL(
    oURL = oURL,
    sbzVersion = sbzHTTPVersion,
    sbzMethod = sbzMethod,
  );
  if sx0Body is not None:
    fApplyBodyToRequest(
      oRequest = oRequest,
      sxBody = sx0Body,
      bCompress = bCompressBody,
      bApplyChunkedEncoding = bApplyChunkedEncodingToBody,
      bSetContentLengthHeader = bAddContentLengthHeaderForBody,
    );

  # Applying form and JSON values sets the Content-Type header. This must be
  # done before we call `fApplyHeaderSettingsToRequest` so the user can
  # overwrite or remove this header later.
  if d0SetForm_sValue_by_sName:
    for (sName, sValue) in d0SetForm_sValue_by_sName.items():
      oRequest.fSetFormValue(sName, sValue);
  if d0SetJSON_xValue_by_sName:
    for (sName, xValue) in d0SetJSON_xValue_by_sName.items():
      oRequest.fSetJSONValue(sName, xValue);
  # Apply headers provided through arguments to request
  fApplyHeaderSettingsToRequest(
    asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
    dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
    atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
    oRequest = oRequest,
  );
  
  return foGetResponseForRequestAndURL(
    oClient = oClient,
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
