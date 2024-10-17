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
  COLOR_WARNING, CHAR_WARNING,
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
  bSaveHTTPResponsesToFiles,
  o0DownloadToFileSystemItem,
  o0SaveHTTPResponsesToFileSystemItem,
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
      bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
      o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
      o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
      bConcatenateDownload = bConcatenateDownload,
      bShowProgress = bShowProgress,
    );
  def fSaveToFile(sMessage, o0TargetFileSystemItem, s0PostfixFileName, sbData):
    def fsGetFileNameFromURLAndResponse():
      # Create a file name that makes sense, given the media type, URL path, and/or host
      sb0MediaType = oResponse.sb0MediaType;
      s0Extension = sb0MediaType and fs0GetExtensionForMediaType(sb0MediaType);
      # No download file name provided; generate one from the URL path if one is provided:
      if oURL.asURLDecodedPath:
        sTargetFileName = oURL.asURLDecodedPath[-1];
        if s0Extension and sb0MediaType != fsb0GetMediaTypeForExtension(sTargetFileName):
          sTargetFileName += "." + s0Extension;
      else:
        sTargetFileName = "download from %s%s" % (
          fsCP437FromBytesString(oURL.sbHost),
          ".%s" % s0Extension if s0Extension else "",
        );
    # Determine target file for download/save
    if o0TargetFileSystemItem is None:
      # User provided no input; generate a file name from the URL and response
      # and save in the current working directory.
      sTargetFileName = fsGetFileNameFromURLAndResponse();
      if s0PostfixFileName:
        sTargetFileName += s0PostfixFileName;
      oTargetFile = cFileSystemItem(sTargetFileName);
    elif o0TargetFileSystemItem.fbIsFolder():
      # User provided a folder as input; generate a file name from the URL and response
      # and create a file in the provided folder.
      oTargetFolder = o0TargetFileSystemItem;
      sTargetFileName = fsGetFileNameFromURLAndResponse();
      oTargetFile = oTargetFolder.foGetChild(sTargetFileName);
    else:
      # User provided a path that is not a folder; assume it is a file path.
      oTargetFile = o0TargetFileSystemItem;
    oConsole.fStatus(
      "      ",
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " ", sMessage, " to file ",
      COLOR_INFO, oTargetFile.sPath,
      COLOR_NORMAL, "...",
    );
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
        COLOR_NORMAL, " Wrote ",
        COLOR_INFO, fsBytesToHumanReadableString(len(sbData)),
        COLOR_NORMAL, " to ",
        COLOR_INFO, oTargetFile.sPath,
        COLOR_NORMAL, "."
      );
  if bSaveHTTPResponsesToFiles:
    fSaveToFile(
      sMessage = "Saving HTTP response",
      o0TargetFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
      s0PostfixFileName = ".http",
      sbData = oResponse.fsbSerialize(),
    );
  if bDownloadToFile:
    if oResponse.uStatusCode != 200:
      oConsole.fOutput(
        "      ",
        COLOR_WARNING, CHAR_WARNING,
        COLOR_NORMAL, " The server returned a ",
        COLOR_INFO, "HTTP %s" % oResponse.uStatusCode,
        COLOR_NORMAL, " response; the downloaded file may not contain what you expect!",
      );
    fSaveToFile(
      sMessage = "Downloading",
      o0TargetFileSystemItem = o0DownloadToFileSystemItem,
      s0PostfixFileName = None,
      sbData = oResponse.fsb0GetDecompressedBody(bTryOtherCompressionTypesOnFailure = not bFailOnDecodeBodyErrors) or b"",
    );
  return oResponse;
