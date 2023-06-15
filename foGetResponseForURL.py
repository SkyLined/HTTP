import sys;

from mFileSystemItem import cFileSystemItem;
from mHumanReadable import fsBytesToHumanReadableString;
from mNotProvided import fbIsProvided, zNotProvided;
from mHTTPProtocol import cURL, fs0GetExtensionForMediaType, fsb0GetMediaTypeForExtension;

from foConsoleLoader import foConsoleLoader;
from fOutputExceptionAndExit import fOutputExceptionAndExit;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mExitCodes import *;
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
  bFixDecodeBodyErrors,
  bSaveToFile,
  s0TargetFilePath,
  bConcatinateDownload,
  bShowProgress,
):
  if d0Form_sValue_by_sName is not None and not fbIsProvided(sbzMethod):
    sbzMethod = "POST";
  # Construct the HTTP request
  oRequest = oHTTPClient.foGetRequestForURL(
    oURL = oURL,
    sbzVersion = sbzHTTPVersion,
    sbzMethod = sbzMethod,
    sb0Body = sb0RequestBody,
    s0Data = s0RequestData,
  );
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
  # Send the request and get the response.
  oConsole.fStatus(
    "      ",
    COLOR_BUSY, CHAR_BUSY,
    COLOR_NORMAL, " Sending request ",
    COLOR_INFO, fsCP437FromBytesString(oRequest.sbVersion),
      " ", fsCP437FromBytesString(oRequest.sbMethod),
      " ", fsCP437FromBytesString(oURL.sbAbsolute),
    COLOR_NORMAL, "...",
  );
  try:
    o0Response = oHTTPClient.fo0GetResponseForRequestAndURL(oRequest, oURL);
  except Exception as oException:
    if isinstance(oException, oHTTPClient.cTCPIPConnectTimeoutException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Connecting to server timed out.",
      );
    elif isinstance(oException, (
      oHTTPClient.cTCPIPConnectionRefusedException,
      oHTTPClient.cTCPIPInvalidAddressException,
      oHTTPClient.cTCPIPDNSUnknownHostnameException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server.",
      );
    elif isinstance(oException, (
      oHTTPClient.cTCPIPConnectionDisconnectedException,
      oHTTPClient.cTCPIPConnectionShutdownException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server did not respond to our request.",
      );
    elif isinstance(oException, oHTTPClient.cHTTPClientFailedToConnectToServerThroughProxyException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server through proxy.",
      );
    elif isinstance(oException, (
      oHTTPClient.cHTTPMaxConnectionsToServerReachedException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server.",
      );
    elif isinstance(oException, oHTTPClient.cTCPIPDataTimeoutException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server was unable to respond in a timely manner.",
      );
    elif isinstance(oException, (
      oHTTPClient.cHTTPOutOfBandDataException,
      oHTTPClient.cHTTPInvalidMessageException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " There was a protocol error while talking to the server.",
      );
    elif oHTTPClient.bSSLIsSupported and isinstance(oException, oHTTPClient.cSSLSecureTimeoutException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server timed out.",
      );
    elif oHTTPClient.bSSLIsSupported and isinstance(oException, oHTTPClient.cSSLException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server failed.",
      );
      o0SSLContext = oException.dxDetails.get("oSSLContext");
      if o0SSLContext:
        for sLine in o0SSLContext.fasGetDetails():
          oConsole.fOutput(
            "          ", sLine,
          );
      d0xPeerCertificate = oException.dxDetails.get("dxPeerCertificate");
      if d0xPeerCertificate:
        for (sName, xValue) in d0xPeerCertificate.items():
          oConsole.fOutput(
            "          ",
            COLOR_NORMAL, str(sName),
            COLOR_DIM, ": ",
            COLOR_NORMAL, repr(xValue),
          );
    else:
      raise;
    oConsole.fOutput();
    fOutputExceptionAndExit(oException, guExitCodeCannotCreateSecureConnection);
  oConsole.fStatus();
  if not o0Response:
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " No response received.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  oResponse = o0Response;
  # Handle redirects if needed
  if u0MaxRedirects is not None and oResponse.uStatusCode in [301, 302, 303, 307, 308]:
    o0LocationHeader = oResponse.oHeaders.fo0GetUniqueHeaderForName(b"Location");
    if not o0LocationHeader:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirected without a \"",
        COLOR_INFO, "Location",
        COLOR_NORMAL, "\" header.",
      );
      sys.exit(guExitCodeNoValidResponseReceived);
    sbRedirectToURL = o0LocationHeader.sbValue;
    try:
      oURL = cURL.foFromBytesString(sbRedirectToURL);
    except cURL.cHTTPInvalidURLException as oException:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirect to invalid URL ",
        COLOR_INFO, sbRedirectToURL,
        COLOR_NORMAL, ":",
      );
    if bShowProgress:
      oConsole.fOutput(
        "      ",
        COLOR_INFO, ">",
        COLOR_NORMAL, " Redirected to URL: ",
        COLOR_INFO, fsCP437FromBytesString(oURL.sbAbsolute),
        COLOR_NORMAL, ".",
      );
    if u0MaxRedirects == 0:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Too many sequential redirects.",
      );
      sys.exit(guExitCodeTooManyRedirects);
    return foGetResponseForURL(
      oHTTPClient = oHTTPClient,
      oURL = oURL,
      sbzHTTPVersion = sbzHTTPVersion,
      sbzMethod = sbzMethod,
      sb0RequestBody = sb0RequestBody,
      s0RequestData = s0RequestData,
      dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
      d0Form_sValue_by_sName = d0Form_sValue_by_sName,
      u0MaxRedirects = u0MaxRedirects - 1,
      bDownloadToFile = bDownloadToFile,
      bFixDecodeBodyErrors = bFixDecodeBodyErrors,
      bSaveToFile = bSaveToFile,
      s0TargetFilePath = s0TargetFilePath,
      bConcatinateDownload = bConcatinateDownload,
      bShowProgress = bShowProgress,
    );
  if not (bSaveToFile or (bDownloadToFile and oResponse.uStatusCode == 200)):
    return oResponse;
  # Determine target file for download/save
  if s0TargetFilePath is None:
    # Create a file name that makes sense, given the media type, URL path, and/or hostname
    sb0MediaType = oResponse.sb0MediaType;
    s0Extension = sb0MediaType and fs0GetExtensionForMediaType(sb0MediaType);
    # No download file name provided; generate one from the URL path if one is provided:
    if oURL.asURLDecodedPath:
      sTargetFilePath = oURL.asURLDecodedPath[-1];
      if s0Extension and sb0MediaType != fsb0GetMediaTypeForExtension(s0TargetFilePath):
        sTargetFilePath += "." + s0Extension;
    else:
      sTargetFilePath = "download from %s%s" % (
        fsCP437FromBytesString(oURL.sbHostname),
        ".%s" % s0Extension if s0Extension else "",
      );
  else:
    sTargetFilePath = s0TargetFilePath;
  oTargetFile = cFileSystemItem(sTargetFilePath);
  # Download response to file if needed
  if bSaveToFile:
    oConsole.fStatus(
      "      ",
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Saving response to file ",
      COLOR_INFO, oTargetFile.sPath,
      COLOR_NORMAL, "...",
    );
    sbData = oResponse.fsbSerialize();
  else:
    oConsole.fStatus(
      "      ",
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Downloading to file ",
      COLOR_INFO, oTargetFile.sPath,
      COLOR_NORMAL, "...",
    );
    sbData = oResponse.fsb0GetDecompressedBody(bTryOtherCompressionTypesOnFailure = bFixDecodeBodyErrors) or b"";
  try:
    oTargetFile.fbWrite(
      sbData = sbData,
      bAppend = bConcatinateDownload,
      bThrowErrors = True,
    );
  except Exception as oException:
    oConsole.fStatus();
    oConsole.fOutput(
      "      ",
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Cannot write ",
      COLOR_INFO, fsBytesToHumanReadableString(len(sbData)),
      COLOR_NORMAL, "to file ",
      COLOR_INFO, oTargetFile.sPath,
      COLOR_NORMAL, ":",
    );
    fOutputExceptionAndExit(oException, guExitCodeCannotWriteResponseBodyToFile);
  oConsole.fStatus();
  if bShowProgress:
    oConsole.fOutput(
      "      ",
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Saved ",
      COLOR_INFO, fsBytesToHumanReadableString(len(sbData)),
      COLOR_NORMAL, " to ",
      COLOR_INFO, oTargetFile.sPath,
      COLOR_NORMAL, "."
    );
  return oResponse;
