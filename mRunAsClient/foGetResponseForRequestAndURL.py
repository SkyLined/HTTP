import sys;

from mFileSystemItem import cFileSystemItem;
from mHTTPProtocol import (
  cURL,
  fs0GetExtensionForMediaType,
  fsb0GetMediaTypeForExtension,
);
from mHumanReadable import fsBytesToHumanReadableString;

from foConsoleLoader import foConsoleLoader;
from fOutputExceptionAndExit import fOutputExceptionAndExit;
from mExitCodes import (
  guExitCodeCannotCreateSecureConnection,
  guExitCodeCannotWriteResponseBodyToFile,
  guExitCodeNoValidResponseReceived,
  guExitCodeTooManyRedirects,
);
from mColorsAndChars import (
  COLOR_BUSY, CHAR_BUSY,
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
  COLOR_OK, CHAR_OK,
);
from mCP437 import fsCP437FromBytesString;
from mOutputSecureConnectionEvents import fOutputSSLException;
oConsole = foConsoleLoader();

def foGetResponseForRequestAndURL(
  *, 
  oHTTPClient,
  oRequest,
  oURL,
  u0MaxRedirects,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bSaveToFile,
  s0TargetFilePath,
  bConcatenateDownload,
  bShowProgress,
):
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
    elif isinstance(oException, oHTTPClient.cTCPIPNetworkErrorException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " A network error occurred.",
      );
    elif isinstance(oException, (
      oHTTPClient.cTCPIPConnectionRefusedException,
      oHTTPClient.cTCPIPInvalidAddressException,
      oHTTPClient.cTCPIPDNSNameCannotBeResolvedException,
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
      fOutputSSLException(oHTTPClient, oException);
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
      oRedirectToURL = oURL.foFromAbsoluteOrRelativeBytesString(sbRedirectToURL);
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
        COLOR_INFO, fsCP437FromBytesString(oRedirectToURL.sbAbsolute),
        COLOR_NORMAL, ".",
      );
    if u0MaxRedirects == 0:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Too many sequential redirects.",
      );
      sys.exit(guExitCodeTooManyRedirects);
    # Create a new request based on the last one:
    oRedirectedRequest = oRequest.foClone();
    # Update the `Host` header and path in the request to reflect the new URL:
    oRedirectedRequest.oHeaders.fbReplaceHeadersForNameAndValue(b"Host", oRedirectToURL.sbHostAndOptionalPort);
    oRedirectedRequest.sbURL = oRedirectToURL.sbRelative;
    # Delete existing cookies:
    oRedirectedRequest.oHeaders.fbRemoveHeadersForName(b"Cookie");
    # Apply appropriate cookies if we have a cookie store.
    if oHTTPClient.o0CookieStore:
      oHTTPClient.o0CookieStore.fApplyToRequestForURL(oRedirectedRequest, oRedirectToURL);
    if oResponse.uStatusCode in [303]: # AFAIK this only applies to 303.
      oRedirectedRequest.sbMethod = b"GET";
      oRedirectedRequest.oHeaders.fbRemoveHeadersForName(b"Transfer-Encoding");
      oRedirectedRequest.oHeaders.fbRemoveHeadersForName(b"Content-Encoding");
      oRedirectedRequest.oHeaders.fbRemoveHeadersForName(b"Content-Type");
      oRedirectedRequest.o0AdditionalHeaders = None;
      oResponse.sbBody = b"";
    return foGetResponseForRequestAndURL(
      oHTTPClient = oHTTPClient,
      oRequest = oRedirectedRequest,
      oURL = oRedirectToURL,
      u0MaxRedirects = u0MaxRedirects - 1,
      bDownloadToFile = bDownloadToFile,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bSaveToFile = bSaveToFile,
      s0TargetFilePath = s0TargetFilePath,
      bConcatenateDownload = bConcatenateDownload,
      bShowProgress = bShowProgress,
    );
  if not (bSaveToFile or (bDownloadToFile and oResponse.uStatusCode == 200)):
    return oResponse;
  # Determine target file for download/save
  if s0TargetFilePath is None:
    # Create a file name that makes sense, given the media type, URL path, and/or host
    sb0MediaType = oResponse.sb0MediaType;
    s0Extension = sb0MediaType and fs0GetExtensionForMediaType(sb0MediaType);
    # No download file name provided; generate one from the URL path if one is provided:
    if oURL.asURLDecodedPath:
      sTargetFilePath = oURL.asURLDecodedPath[-1];
      if s0Extension and sb0MediaType != fsb0GetMediaTypeForExtension(sTargetFilePath):
        sTargetFilePath += "." + s0Extension;
    else:
      sTargetFilePath = "download from %s%s" % (
        fsCP437FromBytesString(oURL.sbHost),
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
    sbData = oResponse.fsb0GetDecompressedBody(bTryOtherCompressionTypesOnFailure = not bFailOnDecodeBodyErrors) or b"";
  try:
    assert oTargetFile.fbWrite(
      sbData = sbData,
      bAppend = bConcatenateDownload,
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
