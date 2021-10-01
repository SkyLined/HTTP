import sys;

from mConsole import oConsole;
from mFileSystemItem import cFileSystemItem;
from mHumanReadable import fsBytesToHumanReadableString;
from mNotProvided import *;

from fOutputSessionExpiredCookie import fOutputSessionExpiredCookie;
from fOutputSessionInvalidCookieAttributeAndExit import fOutputSessionInvalidCookieAttributeAndExit;
from fOutputSessionSetCookie import fOutputSessionSetCookie;
from fsbGetSessionJSONFromSession import fsbGetSessionJSONFromSession;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mExitCodes import *;

def foGetResponseForURL(
  oHTTPClient,
  o0SessionFile, oSession, 
  oURL, sbzMethod, s0RequestData,
  dsbAdditionalOrRemovedHeaders,
  u0MaxRedirects,
  s0zDownloadToFilePath, bFirstDownload,
  bShowProgress,
):
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
  # Send the request and get the response.
  oConsole.fStatus(
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
    bSSLSupportEnabled = hasattr(mExceptions, "cSSLException");
    if isinstance(oException, mExceptions.cTCPIPConnectTimeoutException):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Connecting to server timed out:",
      );
    elif isinstance(oException, (
      mExceptions.cTCPIPConnectionRefusedException,
      mExceptions.cTCPIPInvalidAddressException,
      mExceptions.cDNSUnknownHostnameException,
    )):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server:",
      );
    elif isinstance(oException, (
      mExceptions.cTCPIPConnectionDisconnectedException,
      mExceptions.cTCPIPConnectionShutdownException,
    )):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server did not respond to our request:",
      );
    elif isinstance(oException, mExceptions.cHTTPFailedToConnectToProxyException):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to proxy server:",
      );
    elif isinstance(oException, (
      mExceptions.cMaxConnectionsReachedException,
    )):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not connect to server:",
      );
    elif isinstance(oException, mExceptions.cTCPIPDataTimeoutException):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The server was unable to respond in a timely manner.",
      );
    elif isinstance(oException, (
      mExceptions.cHTTPOutOfBandDataException,
      mExceptions.cHTTPInvalidMessageException,
    )):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " There was a protocol error while talking to the server:",
      );
    elif bSSLSupportEnabled and isinstance(oException, mExceptions.cSSLSecureTimeoutException):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server timed out:",
      );
    elif bSSLSupportEnabled and isinstance(oException, (
      mExceptions.cSSLWrapSocketException,
      mExceptions.cSSLSecureHandshakeException,
      mExceptions.cSSLCannotGetRemoteCertificateException,
      mExceptions.cSSLIncorrectHostnameException,
    )):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Securing the connection to the server failed:",
      );
    else:
      raise;
    fOutputExceptionAndExit(oException, guExitCodeCannotCreateSecureConnection);
  oConsole.fStatus();
  if not o0Response:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " No response received.",
    );
    sys.exit(guExitCodeNoValidResponseReceived);
  oResponse = o0Response;
  # Apply response to session and save session to file if needed
  def fSessionInvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbAttributeName, sbAttributeValue, bIsNameKnown):
    fOutputSessionInvalidCookieAttributeAndExit(oURL.sbOrigin, sbCookieName, sbCookieValue, sbAttributeName, sbAttributeValue, bIsNameKnown);
  def fSessionAddedCookieCallback(oResponse, oURL, oCookie, bIsNewCookie):
    fOutputSessionSetCookie(oURL.sbOrigin, oCookie, bIsNewCookie, not bIsNewCookie); # 3rd argument: cookie is added, 4rth argument: cookie is modified.
  oSession.fUpdateFromResponse(
    oResponse,
    oURL,
    f0InvalidCookieAttributeCallback = fSessionInvalidCookieAttributeCallback,
    f0AddedCookieCallback = fSessionAddedCookieCallback if bShowProgress else None,
    f0ExpiredCookieCallback = fOutputSessionExpiredCookie if bShowProgress else None,
  );
  if o0SessionFile is not None:
    sbSessionJSON = fsbGetSessionJSONFromSession(oSession);
    if bShowProgress:
      oConsole.fStatus(
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
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirected without a \"",
        COLOR_INFO, "Location",
        COLOR_NORMAL, "\" header.",
      );
      sys.exit(guExitCodeNoValidResponseReceived);
    sbRedirectToURL = oLocationHeader.sbValue;
    try:
      oURL = cURL.foFromBytesString(sbRedirectToURL);
    except mExceptions.cInvalidURLException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Redirect to invalid URL ",
        COLOR_INFO, sbRedirectToURL,
        COLOR_NORMAL, ":",
      );
    if bShowProgress:
      oConsole.fOutput(">>> Redirected to URL: ", COLOR_INFO, fsCP437FromBytesString(oURL.sbAbsolute), COLOR_NORMAL, ".");
    if u0MaxRedirects == 0:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Too many sequential redirects.",
      );
      sys.exit(guExitCodeTooManyRedirects);
    return foGetResponseForURL(
      oHTTPClient,
      o0SessionFile, oSession,
      oURL, sbzMethod, s0RequestData,
      dsbAdditionalOrRemovedHeaders,
      u0MaxRedirects - 1,
      s0zDownloadToFilePath, bFirstDownload,
      bShowProgress,
    );
  # Download response to file if needed
  if fbIsProvided(s0zDownloadToFilePath) and oResponse.uStatusCode == 200:
    if s0zDownloadToFilePath is None:
      s0zDownloadToFilePath = oURL.asPath[-1];
    oDownloadToFile = cFileSystemItem(s0zDownloadToFilePath);
    oConsole.fStatus(
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Saving response to file ",
      COLOR_INFO, oDownloadToFile.sPath,
      COLOR_NORMAL, "...",
    );
    if not bFirstDownload:
      oDownloadToFile.fbOpenAsFile(bWritable = True, bAppend = True);
    sb0DecompressedBody = oResponse.sb0DecompressedBody or "";
    try:
      oDownloadToFile.fbWrite(sb0DecompressedBody, bThrowErrors = True);
    except Exception as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, "Cannot write ",
        COLOR_INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)),
        COLOR_NORMAL, "to file ",
        COLOR_INFO, oDownloadToFile.sPath,
        COLOR_NORMAL, ":",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotWriteResponseBodyToFile);
    if oDownloadToFile.fbIsOpenAsFile():
      oDownloadToFile.fbClose();
    oConsole.fStatus();
    if bShowProgress:
      oConsole.fOutput(
        COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Saved ",
        COLOR_INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)),
        COLOR_NORMAL, " to ",
        COLOR_INFO, oDownloadToFile.sPath,
        COLOR_NORMAL, "."
      );
  return oResponse;