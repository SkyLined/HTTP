import json, sys;

from mFileSystemItem import cFileSystemItem;
from mHTTPClient import (
  cHTTPClient,
  cHTTPClientUsingAutomaticProxyServer,
  cHTTPClientUsingProxyServer,
);
from mHTTPCookieStore import cHTTPCookieStore;
from mNotProvided import fbIsProvided;

from foConsoleLoader import foConsoleLoader;
from fOutputExceptionAndExit import fOutputExceptionAndExit;
from mColorsAndChars import (
  COLOR_BUSY, CHAR_BUSY,
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO, CHAR_INFO,
  COLOR_HILITE,
  COLOR_NORMAL,
  COLOR_OK, CHAR_OK
);
from mExitCodes import (
  guExitCodeCannotReadCookiesFromFile,
  guExitCodeCannotWriteCookiesToFile,
  guExitCodeBadArgument,
);
from mOutputConnectionEvents import (
  fOutputFromClientToServerConnecting,
  fOutputFromClientToServerConnectingFailed,
  fOutputFromClientToServerConnectionCreated,
  fOutputFromClientToServerConnectionTerminated,
  
  fOutputFromClientToProxyConnecting,
  fOutputFromClientToProxyConnectingFailed,
  fOutputFromClientToProxyConnectionCreated,
  fOutputFromClientToProxyConnectionTerminated,
  
  fOutputFromClientToServerThroughProxyConnecting,
  fOutputFromClientToServerThroughProxyConnectingFailed,
  fOutputFromClientToServerThroughProxyConnectionCreated,
  fOutputFromClientToServerThroughProxyConnectionTerminated,
);
from mOutputHostEvents import (
  fOutputProxyHostInvalid,
  fOutputProxyHostnameResolvedToIPAddress,
  fOutputResolvingProxyHostname,
  fOutputResolvingProxyHostnameFailed,
  fOutputResolvingServerHostname,
  fOutputResolvingServerHostnameFailed,
  fOutputServerHostInvalid,
  fOutputServerHostnameResolvedToIPAddress,
  fOutputServerHostSpoofed,
);
from mOutputHTTPMessageEvents import (
  fOutputFromClientToServerSendingRequest,
  fOutputFromClientToServerSendingRequestFailed,
  fOutputFromClientToServerRequestSent,  
  fOutputToClientFromServerReceivingResponse,
  fOutputToClientFromServerReceivingResponseFailed,
  fOutputToClientFromServerResponseReceived,
  fOutputFromClientToProxySendingRequest,
  fOutputFromClientToProxySendingRequestFailed,
  fOutputFromClientToProxyRequestSent,
  fOutputToClientFromProxyReceivingResponse,
  fOutputToClientFromProxyReceivingResponseFailed,
  fOutputToClientFromProxyResponseReceived,
);
from mOutputHTTPMessageComponents import (
  fOutputHTTPRequest,
  fOutputHTTPResponse,
);
from mOutputSecureConnectionEvents import (
  fOutputFromClientToServerSecuringConnection,
  fOutputFromClientToServerSecuringConnectionFailed,
  fOutputFromClientToServerConnectionSecured,
  
  fOutputFromClientToProxySecuringConnection,
  fOutputFromClientToProxySecuringConnectionFailed,
  fOutputFromClientToProxyConnectionSecured,

  fOutputFromClientToServerThroughProxySecuringConnection,
  fOutputFromClientToServerThroughProxySecuringConnectionFailed,
  fOutputFromClientToServerThroughProxyConnectionSecured,
);
from mOutputCookieEvents import (
  fOutputInvalidCookieAttribute,
  fOutputCookieSet,
);
oConsole = foConsoleLoader();

def foGetHTTPClient(
  *,
  bUseProxy,
  o0HTTPProxyServerURL,
  n0zTimeoutInSeconds,
  nSendDelayPerByteInSeconds,
  bDecodeBodyOfHTTPMessages,
  bFailOnDecodeBodyErrors,
  bForceHexOutputOfHTTPMessageBody,
  bVerifyCertificates,
  bShowMessageBody,
  bShowProgress,
  bShowRequest,
  bShowResponse,
  bShowDetails,
  uHexOutputCharsPerLine,
  o0NetscapeCookiesFileSystemItem,
  bSaveCookieStore,
  o0CookieStoreJSONFileSystemItem,
  dsbSpoofedHost_by_sbHost,
):
  ### COOKIE STORE ###########################################################
  if bSaveCookieStore:
    oCookieStoreJSONFileSystemItem = o0CookieStoreJSONFileSystemItem or cFileSystemItem("HTTPCookieStore.json");
    bCookieStoreFileExists = oCookieStoreJSONFileSystemItem.fbIsFile();
    def fSaveCookiesToDiskAndOutputSetCookie(oCookieStore, oCookie, o0PreviousCookie):
      dxJSON = oCookieStore.fdxExportToJSON();
      sbJSON = bytes(json.dumps(dxJSON), "ascii", "strict");
      if bShowProgress:
        oConsole.fStatus(
          "      ",
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Saving cookie store to file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        oCookieStoreJSONFileSystemItem.fWrite(sbJSON);
      except Exception as oException:
        oConsole.fStatus();
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not write cookie store file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, "!",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotWriteCookiesToFile);
      oConsole.fStatus();
      fOutputCookieSet(oCookieStore, oCookie, o0PreviousCookie);
  else:
    bCookieStoreFileExists = False;
  oCookieStore = cHTTPCookieStore(
    f0InvalidCookieAttributeCallback = fOutputInvalidCookieAttribute,
    f0SetCookieCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookieStore else fOutputCookieSet,
    f0CookieExpiredCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookieStore else fOutputCookieSet,
    f0CookieAppliedCallback = None, # (oRequest, oURL, oCookie)
    f0HeaderAppliedCallback = None, # (oRequest, oURL, oHeader)
    f0CookieReceivedCallback = None, # (oResponse, oURL, oCookie)
  );
  if o0NetscapeCookiesFileSystemItem:
    if not o0NetscapeCookiesFileSystemItem.fbIsFile():
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Netscape cookies file ",
        COLOR_INFO, o0NetscapeCookiesFileSystemItem.sPath,
        COLOR_NORMAL, " does not exist!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
    if bShowProgress:
      oConsole.fStatus(
        "      ",
        COLOR_BUSY, CHAR_BUSY,
        COLOR_NORMAL, " Reading cookies from file ",
        COLOR_INFO, o0NetscapeCookiesFileSystemItem.sPath,
        COLOR_NORMAL, "...",
      );
    try:
      sbCookiesInNetscapeFileFormat = o0NetscapeCookiesFileSystemItem.fsbRead();
    except Exception as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not read Netscape cookies file ",
        COLOR_INFO, o0NetscapeCookiesFileSystemItem.sPath,
        COLOR_NORMAL, "!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
    try:
      uNumberOfCookiesRead = oCookieStore.fuAddFromNetscapeFileFormat(sbCookiesInNetscapeFileFormat);
    except ValueError as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not read cookies from Netscape cookies file ",
        COLOR_INFO, o0NetscapeCookiesFileSystemItem.sPath,
        COLOR_NORMAL, "!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);

    oConsole.fStatus();
    if bShowProgress:
      oConsole.fOutput(
        COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Read ",
        COLOR_INFO, str(uNumberOfCookiesRead),
        COLOR_HILITE, " cookies from ",
        COLOR_INFO, o0NetscapeCookiesFileSystemItem.sPath,
        COLOR_NORMAL, ".",
      );
  ### HTTP CLIENT ###########################################################
  # We need to use a HTTP client with no proxy, a static proxy or a dynamic
  # proxy. We'll create an instance of the right type of HTTP client now and
  # add event handlers for reporting requests and responses to the user.
  
  # Since the event arguments differ for each type of HTTP client, event
  # handlers specific to the client are created which call into the following
  # two generic functions for reporting the requests/responses:
  if not bUseProxy:
    # Create a HTTP client instance that uses no proxy
    oHTTPClient = cHTTPClient(
      o0CookieStore = oCookieStore,
      n0zConnectTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      bVerifyCertificates = bVerifyCertificates,
      dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
    );
  elif o0HTTPProxyServerURL:
    # Create a HTTP client instance that uses a static proxy
    oHTTPClient = cHTTPClientUsingProxyServer(
      o0HTTPProxyServerURL, 
      o0CookieStore = oCookieStore,
      n0zConnectToProxyTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureConnectionToProxyTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureConnectionToServerTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      bVerifyCertificates = bVerifyCertificates,
    );
  else:
    # Create a HTTP client instance that uses dynamic proxies.
    oHTTPClient = cHTTPClientUsingAutomaticProxyServer(
      o0CookieStore = oCookieStore,
      n0zConnectTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      bVerifyCertificates = bVerifyCertificates,
    );
  if isinstance(oHTTPClient, (cHTTPClient, cHTTPClientUsingAutomaticProxyServer)):
    oHTTPClient.fAddCallbacks({
      "sending request to server": lambda oHTTPClient, *, oConnection, oRequest: (
        bShowProgress and fOutputFromClientToServerSendingRequest(
          oConnection = oConnection,
          oRequest = oRequest,
        ),
      ),
      "sending request to server failed": lambda oHTTPClient, *, oConnection, oRequest, oException: (
        bShowProgress and fOutputFromClientToServerSendingRequestFailed(
          oConnection = oConnection,
          oRequest = oRequest,
          oException = oException,
        ),
      ),
      "sent request to server": lambda oHTTPClient, *, oConnection, oRequest: (
        bShowProgress and fOutputFromClientToServerRequestSent(
          oConnection = oConnection,
          oRequest = oRequest,
        ),
        bShowRequest and fOutputHTTPRequest(
          oRequest,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          bShowDetails = bShowDetails,
          bShowMessageBody = bShowMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
      "receiving response from server": lambda oHTTPClient, *, oConnection, o0Request: (
        bShowProgress and fOutputToClientFromServerReceivingResponse(
          oConnection = oConnection,
        ),
      ),
      "receiving response from server failed": lambda oHTTPClient, *, oConnection, o0Request, oException: (
        bShowProgress and fOutputToClientFromServerReceivingResponseFailed(
          oConnection = oConnection,
          oException = oException,
        ),
      ),
      "received response from server": lambda oHTTPClient, *, oConnection, o0Request, oResponse: (
        bShowProgress and fOutputToClientFromServerResponseReceived(
          oConnection = oConnection,
          oResponse = oResponse,
        ),
        bShowResponse and fOutputHTTPResponse(
          oResponse,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          bShowDetails = bShowDetails,
          bShowMessageBody = bShowMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
    });
  if isinstance(oHTTPClient, (cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer)):
    oHTTPClient.fAddCallbacks({
      "sending request to proxy": lambda oHTTPClient, *, oProxyServerURL, oConnection, oRequest: (
        bShowProgress and fOutputFromClientToProxySendingRequest(
          oConnection = oConnection,
          oRequest = oRequest,
          oProxyServerURL = oProxyServerURL,
        ),
      ),
      "sending request to proxy failed": lambda oHTTPClient, *, oProxyServerURL, oConnection, oRequest, oException: (
        bShowProgress and fOutputFromClientToProxySendingRequestFailed(
          oConnection = oConnection,
          oRequest = oRequest,
          oProxyServerURL = oProxyServerURL,
          oException = oException,
        ),
      ),
      "sent request to proxy": lambda oHTTPClient, *, oProxyServerURL, oConnection, oRequest: (
        bShowProgress and fOutputFromClientToProxyRequestSent(
          oConnection = oConnection,
          oRequest = oRequest,
          oProxyServerURL = oProxyServerURL,
        ),
        # We'll show the request now if we don't also show the response
        bShowRequest and not bShowResponse and fOutputHTTPRequest(
          oRequest,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          bShowDetails = bShowDetails,
          bShowMessageBody = bShowMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
      "receiving response from proxy": lambda oHTTPClient, *, oProxyServerURL, oConnection, o0Request: (
        bShowProgress and fOutputToClientFromProxyReceivingResponse(
          oConnection = oConnection,
          oProxyServerURL = oProxyServerURL,
        ),
      ),
      "receiving response from proxy failed": lambda oHTTPClient, *, oProxyServerURL, oConnection, o0Request, oException: (
        bShowProgress and fOutputToClientFromProxyReceivingResponseFailed(
          oConnection = oConnection,
          oProxyServerURL = oProxyServerURL,
          oException = oException,
        ),
      ),
      "received response from proxy": lambda oHTTPClient, *, oProxyServerURL, oConnection, o0Request, oResponse: (
        bShowProgress and fOutputToClientFromProxyResponseReceived(
          oConnection = oConnection,
          oResponse = oResponse,
          oProxyServerURL = oProxyServerURL,
        ),
        # We'll show the request right before the response if we show both
        bShowRequest and bShowResponse and fOutputHTTPRequest(
          o0Request,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          bShowDetails = bShowDetails,
          bShowMessageBody = bShowMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
        bShowResponse and fOutputHTTPResponse(
          oResponse,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
    });

  if isinstance(oHTTPClient, (cHTTPClient,)):
    oHTTPClient.fAddCallbacks({
      "spoofing server host": fOutputServerHostSpoofed,
    });
  if isinstance(oHTTPClient, (cHTTPClient, cHTTPClientUsingAutomaticProxyServer)):
    oHTTPClient.fAddCallbacks({
      "server host invalid": fOutputServerHostInvalid,
      
      "resolving server hostname to ip address": fOutputResolvingServerHostname,
      "resolving server hostname to ip address failed": fOutputResolvingServerHostnameFailed,
      "resolved server hostname to ip address": fOutputServerHostnameResolvedToIPAddress,
      
      "creating connection to server": fOutputFromClientToServerConnecting,
      "creating connection to server failed": fOutputFromClientToServerConnectingFailed,
      "created connection to server": fOutputFromClientToServerConnectionCreated,
      "terminated connection to server": fOutputFromClientToServerConnectionTerminated,

      "securing connection to server": fOutputFromClientToServerSecuringConnection,
      "securing connection to server failed": fOutputFromClientToServerSecuringConnectionFailed,
      "secured connection to server": fOutputFromClientToServerConnectionSecured,
    });
  if isinstance(oHTTPClient, (cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer)):
    oHTTPClient.fAddCallbacks({
      "proxy host invalid": fOutputProxyHostInvalid,
      "resolving proxy hostname to ip address": fOutputResolvingProxyHostname,
      "resolving proxy hostname to ip address failed": fOutputResolvingProxyHostnameFailed,
      "resolved proxy hostname to ip address": fOutputProxyHostnameResolvedToIPAddress,
      
      "creating connection to proxy": fOutputFromClientToProxyConnecting,
      "creating connection to proxy failed": fOutputFromClientToProxyConnectingFailed,
      "created connection to proxy": fOutputFromClientToProxyConnectionCreated,
      "terminated connection to proxy": fOutputFromClientToProxyConnectionTerminated,

      "securing connection to proxy": fOutputFromClientToProxySecuringConnection,
      "securing connection to proxy failed": fOutputFromClientToProxySecuringConnectionFailed,
      "secured connection to proxy": fOutputFromClientToProxyConnectionSecured,

      "creating connection to server through proxy": fOutputFromClientToServerThroughProxyConnecting,
      "creating connection to server through proxy failed": fOutputFromClientToServerThroughProxyConnectingFailed,
      "created connection to server through proxy": fOutputFromClientToServerThroughProxyConnectionCreated,
      "terminated connection to server through proxy": fOutputFromClientToServerThroughProxyConnectionTerminated,

      "securing connection to server through proxy": fOutputFromClientToServerThroughProxySecuringConnection,
      "securing connection to server through proxy failed": fOutputFromClientToServerThroughProxySecuringConnectionFailed,
      "secured connection to server through proxy": fOutputFromClientToServerThroughProxyConnectionSecured,
    });

  if bSaveCookieStore:
    if bCookieStoreFileExists:
      if bShowProgress:
        oConsole.fOutput(
          "      ",
          COLOR_INFO, CHAR_INFO,
          COLOR_NORMAL, " Cookie store settings:",
        );
        oConsole.fStatus(
          "      ",
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Loading cookie store from file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        sbCookieStoreJSON = oCookieStoreJSONFileSystemItem.fsbRead();
      except Exception as oException:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not read cookie store file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
      if bShowProgress:
        oConsole.fStatus(
          "      ",
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Parsing cookie store file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        dxCookieStoreJSON = json.loads(str(sbCookieStoreJSON, "ascii", "strict"));
      except ValueError as oException:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not parse cookie store file ",
          COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
          COLOR_NORMAL, ":",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
      bJSONHasData = oCookieStore.fbImportFromJSON(dxCookieStoreJSON);
      if bShowProgress and not bJSONHasData:
        oConsole.fOutput(
          "      ",
          "(cookie store file contains no cookie store data).",
        );
    elif (
      not oCookieStoreJSONFileSystemItem.o0Parent
      or not oCookieStoreJSONFileSystemItem.o0Parent.fbIsFolder()
    ):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not find cookie store file ",
        COLOR_INFO, oCookieStoreJSONFileSystemItem.sPath,
        COLOR_NORMAL, " or the folder in which it is located.",
      );
      sys.exit(guExitCodeBadArgument);
  return oHTTPClient;