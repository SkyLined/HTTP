import sys;

from mFileSystemItem import cFileSystemItem;
from mHTTPClient import (
  cClientFailedToConnectToServerThroughProxyException,
);
from mHTTPConnection import (
  cMaximumNumberOfConnectionsToServerReachedException,
);
from mHTTPProtocol import (
  cInvalidMessageException,
  cInvalidURLException,
  fs0GetExtensionForMediaType,
  fsb0GetMediaTypeForExtension,
);
try:
  from mSSL import (
    cSSLException as c0SSLException,
  );
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mSSL'":
    raise;
  c0SSLException = None;
from mTCPIPConnection import (
  cTCPIPConnectionDisconnectedException,
  cTCPIPConnectionRefusedException,
  cTCPIPConnectionShutdownException,
  cTCPIPDataTimeoutException,
  cTCPIPDNSNameCannotBeResolvedException,
  cTCPIPInvalidAddressException,
);
from mHumanReadable import fsBytesToHumanReadableString;
from mTCPIPConnection import (
  cTCPIPConnectTimeoutException,
  cTCPIPNetworkErrorException,
)

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
oConsole = foConsoleLoader();

def foGetResponseForRequestAndURL(
  *, 
  oClient,
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
  try:
    o0Response = oClient.fo0GetResponseForRequestAndURL(oRequest, oURL);
  except Exception as oException:
    if isinstance(oException, cTCPIPConnectTimeoutException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Connecting to server timed out.",
      );
    elif isinstance(oException, cTCPIPNetworkErrorException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " A network error occurred.",
      );
    elif isinstance(oException, (
      cTCPIPConnectionRefusedException,
      cTCPIPInvalidAddressException,
      cTCPIPDNSNameCannotBeResolvedException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server.",
      );
    elif isinstance(oException, (
      cTCPIPConnectionDisconnectedException,
      cTCPIPConnectionShutdownException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server did not respond to our request.",
      );
    elif isinstance(oException, (
      cClientFailedToConnectToServerThroughProxyException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server through proxy.",
      );
    elif isinstance(oException, (
      cMaximumNumberOfConnectionsToServerReachedException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server.",
      );
    elif isinstance(oException, (
      cTCPIPDataTimeoutException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server was unable to respond in a timely manner.",
      );
    elif isinstance(oException, (
      cInvalidMessageException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " There was a protocol error while talking to the server.",
      );
    elif c0SSLException is not None and isinstance(oException, (
      c0SSLException,
    )):
      pass; # We have already provided enough output
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
    aoLocationHeaders = oResponse.oHeaders.faoGetForNormalizedName(b"Location");
    if len(aoLocationHeaders) == 0:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirected without a \"",
        COLOR_INFO, "Location",
        COLOR_NORMAL, "\" header.",
      );
      sys.exit(guExitCodeNoValidResponseReceived);
    if len(aoLocationHeaders) > 1:
      oConsole.fOutput(
        "      ",
        COLOR_WARNING, CHAR_WARNING,
        COLOR_NORMAL, " Redirected with multiple \"",
        COLOR_INFO, "Location",
        COLOR_NORMAL, "\" headers:",
      );
      for oLocationHeader in aoLocationHeaders[:-1]:
        oConsole.fOutput(
          "        ",
          COLOR_NORMAL, "• ",
          COLOR_INFO, fsCP437FromBytesString(oLocationHeader.sbValue),
          COLOR_NORMAL, " (ignored)",
        );
      oConsole.fOutput(
        "        ",
        COLOR_NORMAL, "► ",
        COLOR_INFO, fsCP437FromBytesString(aoLocationHeaders[-1].sbValue),
        COLOR_NORMAL, " (used for redirect).",
      );
    oLocationHeader = aoLocationHeaders[-1];
    sbRedirectToURL = oLocationHeader.sbValue;
    try:
      oRedirectToURL = oURL.foFromAbsoluteOrRelativeBytesString(sbRedirectToURL);
    except cInvalidURLException as oException:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirect to invalid URL ",
        COLOR_INFO, fsCP437FromBytesString(sbRedirectToURL),
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
    oRedirectedRequest.oHeaders.foReplaceOrAddUniqueNameAndValue(b"Host", oRedirectToURL.sbHostAndOptionalPort);
    oRedirectedRequest.sbURL = oRedirectToURL.sbRelative;
    # Delete existing cookies:
    oRedirectedRequest.oHeaders.fbRemoveForNormalizedName(b"Cookie");
    # Apply appropriate cookies if we have a cookie store.
    if oClient.o0CookieStore:
      oClient.o0CookieStore.fApplyToRequestForURL(oRedirectedRequest, oRedirectToURL);
    if oResponse.uStatusCode in [303]: # AFAIK this only applies to 303.
      oRedirectedRequest.sbMethod = b"GET";
      oRedirectedRequest.oHeaders.fbRemoveForNormalizedName(b"Transfer-Encoding");
      oRedirectedRequest.oHeaders.fbRemoveForNormalizedName(b"Content-Encoding");
      oRedirectedRequest.oHeaders.fbRemoveForNormalizedName(b"Content-Type");
      oRedirectedRequest.o0AdditionalHeaders = None;
      oResponse.sbBody = b"";
    return foGetResponseForRequestAndURL(
      oClient = oClient,
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
      return sTargetFileName;
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
    if bFailOnDecodeBodyErrors:
      sbResponseData = oResponse.fsbGetOptionallyChunkedDecodedAndDecompressedBody();
    else:
      (sbResponseData, asbActualCompressionTypes) = oResponse.ftxGetOptionallyChunkedDecodedAndDecompressedBodyAndActualCompressionTypes();
    fSaveToFile(
      sMessage = "Downloading",
      o0TargetFileSystemItem = o0DownloadToFileSystemItem,
      s0PostfixFileName = None,
      sbData = sbResponseData,
    );
  return oResponse;
