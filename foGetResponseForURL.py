import sys;

from mFileSystemItem import cFileSystemItem;
from mHumanReadable import fsBytesToHumanReadableString;
from mNotProvided import fbIsProvided, zNotProvided;
from mHTTPProtocol import cURL, fs0GetExtensionForMediaType, fsb0GetMediaTypeForExtension;

from foConsoleLoader import foConsoleLoader;
from fOutputExceptionAndExit import fOutputExceptionAndExit;
from fOutputSessionExpiredCookie import fOutputSessionExpiredCookie;
from fOutputSessionInvalidCookieAttributeAndExit import fOutputSessionInvalidCookieAttributeAndExit;
from fOutputSessionSetCookie import fOutputSessionSetCookie;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mExitCodes import *;
oConsole = foConsoleLoader();

def foGetResponseForURL(
  oHTTPClient,
  o0SessionFile, oSession, 
  oURL, sbzMethod, s0RequestData,
  dsbAdditionalOrRemovedHeaders,
  d0Form_sValue_by_sName,
  u0MaxRedirects,
  s0zDownloadToFilePath, bFirstDownload,
  bShowProgress,
):
  if d0Form_sValue_by_sName is not None and not fbIsProvided(sbzMethod):
    sbzMethod = "POST";
  # Construct the HTTP request
  oRequest = oHTTPClient.foGetRequestForURL(
    oURL = oURL,
    sbzVersion = oSession.sbzHTTPVersion if oSession else zNotProvided,
    sbzMethod = sbzMethod,
    s0Data = s0RequestData,
  );
  # Apply session to request
  oSession.fApplyHeadersToRequestForURL(
    oRequest,
    oURL,
    f0CookieExpiredCallback = fOutputSessionExpiredCookie if bShowProgress else None,
    f0HeaderAppliedCallback = None, # fSessionAppliedHeaderHandler(oRequest, oURL, oHeader, bReplaced)
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
        COLOR_NORMAL, " Connecting to server timed out:",
      );
    elif isinstance(oException, (
      oHTTPClient.cTCPIPConnectionRefusedException,
      oHTTPClient.cTCPIPInvalidAddressException,
      oHTTPClient.cTCPIPDNSUnknownHostnameException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server:",
      );
    elif isinstance(oException, (
      oHTTPClient.cTCPIPConnectionDisconnectedException,
      oHTTPClient.cTCPIPConnectionShutdownException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server did not respond to our request:",
      );
    elif isinstance(oException, oHTTPClient.cHTTPClientFailedToConnectToServerThroughProxyException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server through proxy:",
      );
    elif isinstance(oException, (
      oHTTPClient.cHTTPMaxConnectionsToServerReachedException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server:",
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
        COLOR_NORMAL, " There was a protocol error while talking to the server:",
      );
    elif oHTTPClient.bSSLIsSupported and isinstance(oException, oHTTPClient.cSSLSecureTimeoutException):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server timed out:",
      );
    elif oHTTPClient.bSSLIsSupported and isinstance(oException, (
      oHTTPClient.cSSLWrapSocketException,
      oHTTPClient.cSSLSecureHandshakeException,
      oHTTPClient.cSSLCannotGetRemoteCertificateException,
      oHTTPClient.cSSLIncorrectHostnameException,
    )):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server failed:",
      );
    else:
      raise;
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
  # Apply response to session and save session to file if needed
  def fSessionInvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbAttributeName, sb0AttributeValue, bIsNameKnown):
    fOutputSessionInvalidCookieAttributeAndExit(oURL.sbOrigin, sbCookieName, sbCookieValue, sbAttributeName, sb0AttributeValue, bIsNameKnown);
  def fSessionSetCookieCallback(oResponse, oURL, oCookie, o0PreviousCookie):
    if oCookie.fbIsExpired():
      fOutputSessionExpiredCookie(oURL.sbOrigin, oCookie);
    else:
      fOutputSessionSetCookie(oURL.sbOrigin, oCookie, o0PreviousCookie);
  oSession.fUpdateFromResponse(
    oResponse,
    oURL,
    f0InvalidCookieAttributeCallback = fSessionInvalidCookieAttributeCallback,
    f0SetCookieCallback = fSessionSetCookieCallback if bShowProgress else None,
  );
  if o0SessionFile is not None:
    sbSessionJSON = oSession.fsbExportToJSON();
    if bShowProgress:
      oConsole.fStatus(
        "      ",
        COLOR_BUSY, CHAR_BUSY,
        COLOR_NORMAL, " Saving session to file ",
        COLOR_INFO, o0SessionFile.sPath,
        COLOR_NORMAL, "...",
      );
    try:
      o0SessionFile.fbWrite(sbSessionJSON, bThrowErrors = True);
    except Exception as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not write session file ",
        COLOR_INFO, o0SessionFile.sPath,
        COLOR_NORMAL, "!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotWriteSessionToFile);
    oConsole.fStatus();
  # Handle redirects if needed
  if u0MaxRedirects is not None and oResponse.uStatusCode in [301, 302, 307, 308]:
    oLocationHeader = oResponse.oHeaders.fo0GetUniqueHeaderForName(b"Location");
    if not oLocationHeader:
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirected without a \"",
        COLOR_INFO, "Location",
        COLOR_NORMAL, "\" header.",
      );
      sys.exit(guExitCodeNoValidResponseReceived);
    sbRedirectToURL = oLocationHeader.sbValue;
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
      oHTTPClient,
      o0SessionFile, oSession, 
      oURL, sbzMethod, s0RequestData,
      dsbAdditionalOrRemovedHeaders,
      d0Form_sValue_by_sName,
      u0MaxRedirects - 1,
      s0zDownloadToFilePath, bFirstDownload,
      bShowProgress,
    );
  # Download response to file if needed
  if fbIsProvided(s0zDownloadToFilePath) and oResponse.uStatusCode == 200:
    if s0zDownloadToFilePath is None:
      # Create a file name that makes sense, given the media type, URL path, and/or hostname
      sb0MediaType = oResponse.sb0MediaType;
      s0Extension = sb0MediaType and fs0GetExtensionForMediaType(sb0MediaType);
      # No download file name provided; generate one from the URL path if one is provided:
      if oURL.asURLDecodedPath:
        s0zDownloadToFilePath = oURL.asURLDecodedPath[-1];
        if s0Extension and sb0MediaType != fsb0GetMediaTypeForExtension(s0zDownloadToFilePath):
          s0zDownloadToFilePath += "." + s0Extension;
      else:
        s0zDownloadToFilePath = "download from %s%s" % (
          fsCP437FromBytesString(oURL.sbHostname),
          ".%s" % s0Extension if s0Extension else "",
        );
    oDownloadToFile = cFileSystemItem(s0zDownloadToFilePath);
    oConsole.fStatus(
      "      ",
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Saving response to file ",
      COLOR_INFO, oDownloadToFile.sPath,
      COLOR_NORMAL, "...",
    );
    sb0DecompressedBody = oResponse.sb0DecompressedBody or "";
    try:
      oDownloadToFile.fbWrite(
        sbData = sb0DecompressedBody,
        bAppend = not bFirstDownload,
        bThrowErrors = True,
      );
    except Exception as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Cannot write ",
        COLOR_INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)),
        COLOR_NORMAL, "to file ",
        COLOR_INFO, oDownloadToFile.sPath,
        COLOR_NORMAL, ":",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotWriteResponseBodyToFile);
    oConsole.fStatus();
    if bShowProgress:
      oConsole.fOutput(
        "      ",
        COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Saved ",
        COLOR_INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)),
        COLOR_NORMAL, " to ",
        COLOR_INFO, oDownloadToFile.sPath,
        COLOR_NORMAL, "."
      );
  return oResponse;
