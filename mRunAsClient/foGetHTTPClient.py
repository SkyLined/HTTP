
from mFileSystemItem import cFileSystemItem;
from mHTTPClient import (
  cHTTPClient,
  cHTTPClientUsingAutomaticProxyServer,
  cHTTPClientUsingProxyServer,
);
from mHTTPCookieStore import cHTTPCookieStore;

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
  fOutputConnectionToProxyCreated,
  fOutputConnectingToProxyIPAddress,
  fOutputConnectingToProxyIPAddressFailed,
  fOutputConnectionToProxyTerminated,
  fOutputConnectionToServerCreated,
  fOutputConnectingToServerIPAddress,
  fOutputConnectingToServerIPAddressFailed,
  fOutputConnectionToServerTerminated,
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
from mOutputHTTPClientEvents import (
  fOutputRequestSent,
  fOutputRequestSentAndResponseReceived,
);
from mOutputHTTPMessageComponents import (
  fOutputHTTPRequest,
  fOutputHTTPResponse,
);
from mOutputSecureConnectionEvents import (
  fOutputSecureConnectionToServerThroughProxyCreated,
  fOutputSecureConnectionToServerThroughProxyTerminated,
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
  bVerifyCertificates,
  bShowProgress,
  bShowProxyConnects,
  bShowRequest,
  bShowResponse,
  bShowDetails,
  bDecodeBody,
  bFailOnDecodeBodyErrors,
  bForceHex,
  uHexChars,
  s0NetscapeCookiesFilePath,
  bSaveCookiesToDisk,
  s0zCookieStoreJSONPath,
  dsbSpoofedHost_by_sbHost,
):
  ### COOKIE STORE ###########################################################
  if bSaveCookiesToDisk:
    s0zCookieStoreJSONPath  = s0zCookieStoreJSONPath or "HTTPCookieStore.json";
    oCookieStoreJSONFile = cFileSystemItem(s0zCookieStoreJSONPath);
    bCookieStoreFileExists = oCookieStoreJSONFile.fbIsFile();
    def fSaveCookiesToDiskAndOutputSetCookie(oCookieStore, oCookie, o0PreviousCookie):
      dxJSON = oCookieStore.fdxExportToJSON();
      sbJSON = bytes(json.dumps(dxJSON), "ascii", "strict");
      if bShowProgress:
        oConsole.fStatus(
          "      ",
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Saving cookie store to file ",
          COLOR_INFO, oCookieStoreJSONFile.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        oCookieStoreJSONFile.fWrite(sbJSON);
      except Exception as oException:
        oConsole.fStatus();
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not write cookie store file ",
          COLOR_INFO, oCookieStoreJSONFile.sPath,
          COLOR_NORMAL, "!",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotWriteCookiesToFile);
      oConsole.fStatus();
      fOutputSetCookie(oCookieStore, oCookie, o0PreviousCookie);
  else:
    bCookieStoreFileExists = False;
  oCookieStore = cHTTPCookieStore(
    f0InvalidCookieAttributeCallback = fOutputInvalidCookieAttribute,
    f0SetCookieCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookiesToDisk else fOutputCookieSet,
    f0CookieExpiredCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookiesToDisk else fOutputCookieSet,
    f0CookieAppliedCallback = None, # (oRequest, oURL, oCookie)
    f0HeaderAppliedCallback = None, # (oRequest, oURL, oHeader)
    f0CookieReceivedCallback = None, # (oResponse, oURL, oCookie)
  );
  if s0NetscapeCookiesFilePath:
    oNetscapeCookiesFile = cFileSystemItem(s0NetscapeCookiesFilePath);
    if not oNetscapeCookiesFile.fbIsFile():
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Netscape cookies file ",
        COLOR_INFO, oNetscapeCookiesFile.sPath,
        COLOR_NORMAL, " does not exist!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
    if bShowProgress:
      oConsole.fStatus(
        "      ",
        COLOR_BUSY, CHAR_BUSY,
        COLOR_NORMAL, " Reading cookies from file ",
        COLOR_INFO, oNetscapeCookiesFile.sPath,
        COLOR_NORMAL, "...",
      );
    try:
      sbCookiesInNetscapeFileFormat = oNetscapeCookiesFile.fsbRead();
    except Exception as oException:
      oConsole.fStatus();
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not read Netscape cookies file ",
        COLOR_INFO, oNetscapeCookiesFile.sPath,
        COLOR_NORMAL, "!",
      );
      fOutputExceptionAndExit(oException, guExitCodeCannotWriteCookiesToFile);
    uNumberOfCookiesRead = oCookieStore.fuAddFromNetscapeFileFormat(sbCookiesInNetscapeFileFormat);
    oConsole.fStatus();
    if bShowProgress:
      oConsole.fOutput(
        COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Read ",
        COLOR_INFO, str(uNumberOfCookiesRead),
        COLOR_HILITE, " cookies from ",
        COLOR_INFO, oNetscapeCookiesFile.sPath,
        COLOR_NORMAL, ".",
      );
  ### HTTP CLIENT ###########################################################
  # We need to use a HTTP client with no proxy, a static proxy or a dynamic
  # proxy. We'll create an instance of the right type of HTTP client now and
  # add event handlers for reporting requests and responses to the user.
  
  # Since the event arguments differ for each type of HTTP client, event
  # handlers specific to the client are created which call into the following
  # two generic functions for reporting the requests/reponses:
  if not bUseProxy:
    # Create a HTTP client instance that uses no proxy
    oClient = cHTTPClient(
      o0CookieStore = oCookieStore,
      n0zConnectTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      bVerifyCertificates = bVerifyCertificates,
      dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
    );
  elif o0HTTPProxyServerURL:
    # Create a HTTP client instance that uses a static proxy
    oClient = cHTTPClientUsingProxyServer(
      o0HTTPProxyServerURL, 
      o0CookieStore = oCookieStore,
      n0zConnectToProxyTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureConnectionToProxyTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureConnectionToServerTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      bVerifyCertificates = bVerifyCertificates,
    );
  else:
    # Create a HTTP client instance that uses dynamic proxies.
    oClient = cHTTPClientUsingAutomaticProxyServer(
      o0CookieStore = oCookieStore,
      n0zConnectTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zSecureTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      bVerifyCertificates = bVerifyCertificates,
    );
  if bShowProgress:
    oClient.fAddCallback("request sent", lambda
      oClient,
      *,
      oSecondaryClient = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      o0ProxyServerURL = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      oConnection,
      oRequest:
        fOutputRequestSent(
          oConnection,
          oRequest,
          o0HTTPProxyServerURL,
          bShowProxyConnects,
        ),
    );
    oClient.fAddCallback("request sent and response received", lambda
      oClient,
      *,
      oSecondaryClient = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      o0ProxyServerURL = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      oConnection,
      oRequest,
      oResponse:
        fOutputRequestSentAndResponseReceived(
          oConnection,
          oRequest,
          oResponse,
          o0HTTPProxyServerURL,
          bShowProxyConnects,
        ),
    );
    if isinstance(oClient, (cHTTPClient,)):
      oClient.fAddCallbacks({
        "spoofing server host": fOutputServerHostSpoofed,
      });
    if isinstance(oClient, (cHTTPClient, cHTTPClientUsingAutomaticProxyServer)):
      oClient.fAddCallbacks({
        "server host invalid": fOutputServerHostInvalid,
        
        "resolving server hostname": fOutputResolvingServerHostname,
        "resolving server hostname failed": fOutputResolvingServerHostnameFailed,
        "server hostname resolved to ip address": fOutputServerHostnameResolvedToIPAddress,
        
        "connecting to server ip address": fOutputConnectingToServerIPAddress,
        "connecting to server ip address failed": fOutputConnectingToServerIPAddressFailed,
        # We will always inform the user of this
        # "connecting to server failed": fOutputConnectingToServerFailed,
        "connection to server created": fOutputConnectionToServerCreated,
        "connection to server terminated": fOutputConnectionToServerTerminated,
      });
    if isinstance(oClient, (cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer)):
      oClient.fAddCallbacks({
        "proxy host invalid": fOutputProxyHostInvalid,
        "resolving proxy hostname": fOutputResolvingProxyHostname,
        "resolving proxy hostname failed": fOutputResolvingProxyHostnameFailed,
        "proxy hostname resolved to ip address": fOutputProxyHostnameResolvedToIPAddress,
        
        "connecting to proxy ip address": fOutputConnectingToProxyIPAddress,
        "connecting to proxy ip address failed": fOutputConnectingToProxyIPAddressFailed,
        # We will always inform the user of this
        # "connecting to server failed": fOutputConnectingToServerFailed,
        "connection to proxy created": fOutputConnectionToProxyCreated,
        "connection to proxy terminated": fOutputConnectionToProxyTerminated,
        "secure connection to server through proxy created": fOutputSecureConnectionToServerThroughProxyCreated,
        "secure connection to server through proxy terminated": fOutputSecureConnectionToServerThroughProxyTerminated,
      });
  if bShowRequest:
    oClient.fAddCallback("request sent", lambda
      oClient,
      *,
      oSecondaryClient = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      o0ProxyServerURL = None, # Only provided by cHTTPClientUsingAutomaticProxyServer
      oConnection,
      oRequest:
        fOutputHTTPRequest(
          oRequest,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBody,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHex = bForceHex,
          uHexChars = uHexChars,
          xPrefix = "",
        ),
    );
  if bShowResponse:
    # If we do this with "response received" event, it will fire before we have shown progress (above)
    oClient.fAddCallback("request sent and response received", lambda
      oClient,
      *,
      oSecondaryClient = None,
      o0ProxyServerURL = None,
      oConnection,
      oRequest,
      oResponse:
        fOutputHTTPResponse(
          oResponse,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBody,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHex = bForceHex,
          uHexChars = uHexChars,
          xPrefix = "",
        ),
    );

  if bSaveCookiesToDisk:
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
          COLOR_INFO, oCookieStoreJSONFile.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        sbCookieStoreJSON = oCookieStoreJSONFile.fsbRead();
      except Exception as oException:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not read cookie store file ",
          COLOR_INFO, oCookieStoreJSONFile.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
      if bShowProgress:
        oConsole.fStatus(
          "      ",
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Parsing cookie store file ",
          COLOR_INFO, oCookieStoreJSONFile.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        dxCookieStoreJSON = json.loads(str(sbCookieStoreJSON, "ascii", "strict"));
      except ValueError as oException:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not parse cookie store file ",
          COLOR_INFO, oCookieStoreJSONFile.sPath,
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
      not oCookieStoreJSONFile.o0Parent
      or not oCookieStoreJSONFile.o0Parent.fbIsFolder()
    ):
      oConsole.fOutput(
        "      ",
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not find cookie store file ",
        COLOR_INFO, oCookieStoreJSONFile.sPath,
        COLOR_NORMAL, " or the folder in which it is located.",
      );
      sys.exit(guExitCodeBadArgument);
  return oClient;