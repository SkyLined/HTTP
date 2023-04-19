"""                                                      _   _                  
           ┄┄┄┄┄┄┄┄╒╦╦┄┄╦╦╕┄╒═╦╦═╕┄╒═╦╦═╕┄╒╦╦══╦╗┄┄┄┄┄┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄          
                    ║╠══╣║    ║║     ║║    ║╠══╩╝  □   ╱╱  ╱╱                   
         ┄┄┄┄┄┄┄┄┄┄╘╩╩┄┄╩╩╛┄┄╘╩╩╛┄┄┄╘╩╩╛┄┄╘╩╩╛┄┄┄┄┄□┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄            
                                                      ‾   ‾                  """;
import base64, json, os, re, sys;

sModulePath = os.path.dirname(__file__);
sys.path = [sModulePath] + [sPath for sPath in sys.path if sPath.lower() != sModulePath.lower()];
from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

def fbParseBooleanArgument(s0Value):
  if s0Value is None or s0Value.lower() == "true":
    return True;
  if s0Value.lower() == "false":
    return False;
  oConsole.fOutput(
    COLOR_ERROR, CHAR_ERROR,
    COLOR_NORMAL, " The value for \"",
    COLOR_INFO, sArgument,
    COLOR_NORMAL, "\" must be \"",
    COLOR_INFO, "true",
    COLOR_NORMAL, "\" (default) or \"",
    COLOR_INFO, "false",
    COLOR_NORMAL, "\".",
  );
  sys.exit(guExitCodeBadArgument);

guExitCodeInternalError = 1; # Just in case mExitCodes is not loaded, as we need this later.
try:
  from mFileSystemItem import cFileSystemItem;
  from mHTTPClient import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer, cURL;
  from mHTTPCookieStore import cHTTPCookieStore;
  from mNotProvided import fbIsProvided, zNotProvided;
  
  from faoGetURLsFromM3U import faoGetURLsFromM3U;
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from fHandleServerHostnameOrIPAddressInvalid import fHandleServerHostnameOrIPAddressInvalid;
  from fHandleServerHostnameResolvedToIPAddress import fHandleServerHostnameResolvedToIPAddress;
  from fHandleConnectingToServerIPAddress import fHandleConnectingToServerIPAddress;
  from fHandleConnectingToServerIPAddressFailed import fHandleConnectingToServerIPAddressFailed;
  from fHandleConnectionToServerCreated import fHandleConnectionToServerCreated;
  from fHandleConnectionToServerTerminated import fHandleConnectionToServerTerminated;
  from fHandleProxyHostnameOrIPAddressInvalid import fHandleProxyHostnameOrIPAddressInvalid;
  from fHandleProxyHostnameResolvedToIPAddress import fHandleProxyHostnameResolvedToIPAddress;
  from fHandleConnectingToProxyIPAddress import fHandleConnectingToProxyIPAddress;
  from fHandleConnectingToProxyIPAddressFailed import fHandleConnectingToProxyIPAddressFailed;
  from fHandleConnectionToProxyCreated import fHandleConnectionToProxyCreated;
  from fHandleConnectionToProxyTerminated import fHandleConnectionToProxyTerminated;
  from fHandleSecureConnectionToServerThroughProxyCreated import fHandleSecureConnectionToServerThroughProxyCreated;
  from fHandleSecureConnectionToServerThroughProxyTerminated import fHandleSecureConnectionToServerThroughProxyTerminated;
  from fHandleRequestSent import fHandleRequestSent;
  from fHandleRequestSentAndResponseReceived import fHandleRequestSentAndResponseReceived;
  from fHandleResolvingServerHostname import fHandleResolvingServerHostname;
  from fHandleResolvingServerHostnameFailed import fHandleResolvingServerHostnameFailed;
  from fHandleResolvingProxyHostname import fHandleResolvingProxyHostname;
  from fHandleResolvingProxyHostnameFailed import fHandleResolvingProxyHostnameFailed;
  from foConsoleLoader import foConsoleLoader;
  from foGetResponseForURL import foGetResponseForURL;
  from fOutputInvalidCookieAttributeAndExit import fOutputInvalidCookieAttributeAndExit;
  from fOutputSetCookie import fOutputSetCookie;
  from fOutputExceptionAndExit import fOutputExceptionAndExit;
  from fOutputUsageInformation import fOutputUsageInformation;
  from fOutputRequestSent import fOutputRequestSent;
  from fOutputResponseReceived import fOutputResponseReceived;
  from mColorsAndChars import *;
  from mExitCodes import \
      guExitCodeBadArgument, \
      guExitCodeCannotReadCookiesFromFile, \
      guExitCodeCannotReadRequestBodyFromFile, \
      guExitCodeCannotWriteCookiesToFile, \
      guExitCodeNoValidResponseReceived, \
      guExitCodeSuccess;
  oConsole = foConsoleLoader();
  
  if __name__ == "__main__":
    rShouldBeAURL = re.compile(r"^https?://.*$", re.I);
    rMethod = re.compile(r"^[A-Z]+$", re.I);
    rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
    rCharEncoding = re.compile(r"([^\\]+)|\\(?:x([0-9a-f]{2}))?", re.I);
    arbSegmentedVideos = [re.compile(sb) for sb in [
      (
        rb"("
          rb".*?/"
          rb"(?:\w+\-)+?"
        rb")("
          rb"\d+"
        rb")("
          rb"(?:\-\w+)*"
          rb"\.ts"
          rb"(?:\?.*)?"
        rb")"
      ), (
        rb"("
          rb".*?/"
          rb"(?:\w+\-)+?"
          rb"(?:\w*?)"
        rb")("
          rb"\d+"
        rb")("
          rb"(?:\-\w+)*"
          rb"\.ts"
          rb"(?:\?.*)?"
        rb")"
      )
    ]];
    
    asArguments = sys.argv[1:];
    dsbAdditionalOrRemovedHeaders = {};
    d0Form_sValue_by_sName = {};
    sbzHTTPVersion = zNotProvided;
    sbzMethod = zNotProvided;
    o0URL = None;
    bM3U = False;
    bSegmentedVideo = None;
    uStartIndex = None;
    bzShowProgress = zNotProvided;
    bzShowRequest = zNotProvided;
    bzShowResponse = zNotProvided;
    bzShowDetails = zNotProvided;
    bShowProxyConnects = False;
    bUseProxy = False;
    o0HTTPProxyServerURL = None;
    s0RequestData = None;
    bDecodeBody = False;
    u0MaxRedirects = None;
    bVerifyCertificates = True;
    bSaveToFile = False;
    bDownloadToFile = False;
    s0TargetFilePath = zNotProvided;
    s0zCookieStoreJSONPath = zNotProvided;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      def fsRequireArgumentValue():
        if s0Value:
          return "".join([
            oMatch.group(1) if oMatch.group(1)
                else chr(int(oMatch.group(2), 16)) if oMatch.group(2) else ""
            for oMatch in rCharEncoding.finditer(s0Value)
          ]);
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " You must provide a value for \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      if s0LowerName in ["debug"]:
        if fbParseBooleanArgument(s0Value):
          if not m0DebugOutput:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " The ",
              COLOR_INFO, "mDebugOutput",
              COLOR_NORMAL, " module is needed to show debug information but it is not available!",
            );
            sys.exit(guExitCodeBadArgument);
          m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName in ["data"]:
        s0RequestData = fsRequireArgumentValue();
      elif s0LowerName in ["df", "data-file"]:
        oDataFileSystemItem = cFileSystemItem(fsRequireArgumentValue());
        if not oDataFileSystemItem.fbIsFile():
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot find file \"",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, "\"."
          );
          sys.exit(guExitCodeBadArgument);
        try:
          sbRequestData = oDataFileSystemItem.fsbRead();
          s0RequestData = str(sbRequestData, "utf-8", "strict");
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot read from file ",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, ".",
          );
          fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
      elif s0LowerName in ["db", "decode", "decode-body"]:
        bDecodeBody = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["dl", "download"]:
        bDownloadToFile = True;
        s0TargetFilePath = s0Value;
      elif s0LowerName in ["save"]:
        bSaveToFile = True;
        s0TargetFilePath = s0Value;
      elif s0LowerName in ["s", "store"]:
        s0zCookieStoreJSONPath = s0Value;
      elif s0LowerName in ["header"]:
        sbValue = bytes(ord(s) for s in fsRequireArgumentValue());
        tsbNameAndValue = sbValue.split(b":", 1);
        if len(tsbNameAndValue) == 1:
          sbName = sbValue; sb0Value = None;
        else:
          sbName, sb0Value = tsbNameAndValue;
          if sb0Value.strip() == "":
            sb0Value = None;
        dsbAdditionalOrRemovedHeaders[sbName] = sb0Value;
      elif s0LowerName in ["form"]:
        sbValue = bytes(ord(s) for s in fsRequireArgumentValue());
        tsbNameAndValue = sbValue.split(b"=", 1);
        if len(tsbNameAndValue) == 1:
          sbName = sbValue; sb0Value = "";
        else:
          sbName, sb0Value = tsbNameAndValue;
        if d0Form_sValue_by_sName is None:
          d0Form_sValue_by_sName = [];
        d0Form_sValue_by_sName[sbName] = sb0Value;
      elif s0LowerName in ["basic-login"]:
        sbBase64EncodedUserNameColonPassword = base64.b64encode(bytes(s0Value or "", "ascii", "strict"));
        dsbAdditionalOrRemovedHeaders[b"Authorization"] = b"basic %s" % sbBase64EncodedUserNameColonPassword;
      elif s0LowerName in ["p", "proxy", "http-proxy"]:
        bUseProxy = True;
        if s0Value:
          if o0HTTPProxyServerURL is not None:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " You can only provide one proxy server URL.",
            );
            sys.exit(guExitCodeBadArgument);
          o0HTTPProxyServerURL = cURL.foFromBytesString(bytes(ord(s) for s in s0Value));
      elif s0LowerName in ["r", "max-redirects"]:
        sMaxRedirects = fsRequireArgumentValue();
        try:
          u0MaxRedirects = int(sMaxRedirects);
          assert u0MaxRedirects >= 0, "";
        except:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value for \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" must be a positive integer number or zero.",
          );
          sys.exit(guExitCodeBadArgument);
      elif s0LowerName in ["m3u"]:
        bM3U = True;
        bDownloadToFile = True;
        # If a path is provided for downloading, set it.
        if s0Value is not None:
          s0TargetFilePath = s0Value;
      elif s0LowerName in ["sv", "segmented-video"]:
        bSegmentedVideo = True;
        bDownloadToFile = True;
        # If a path is provided for downloading, set it. If not, make sure we download by setting it to None
        if s0Value:
          s0TargetFilePath = s0Value;
      elif s0LowerName in ["secure"]:
        bVerifyCertificates = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-progress"]:
        bzShowProgress = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-proxy"]:
        bzShowProxyConnects = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-request"]:
        bzShowRequest = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-response"]:
        bzShowResponse = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-details"]:
        bzShowDetails = fbParseBooleanArgument(s0Value);
      elif s0LowerName:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Unknown argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      elif o0URL is None and rShouldBeAURL.match(sArgument):
        try:
          o0URL = cURL.foFromBytesString(bytes(ord(s) for s in sArgument));
        except cURL.cHTTPInvalidURLException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" is not a valid URL.",
          );
          sys.exit(guExitCodeBadArgument);
      elif not fbIsProvided(sbzMethod) and rMethod.match(sArgument):
        sbzMethod = bytes(ord(s) for s in sArgument);
      elif rHTTPVersion.match(sArgument):
        sbzHTTPVersion = bytes(ord(s) for s in sArgument);
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Superfluous argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
    ### DONE PARSING ARGUMENTS #################################################
    if o0URL is None:
      fOutputUsageInformation();
      sys.exit(guExitCodeSuccess);
    oURL = o0URL;
    # If not explicitly set, show progress
    bShowProgress = bzShowProgress if fbIsProvided(bzShowProgress) else True;
    # If not explicitly set, only show requests and responses when we are not downloading.
    bShowRequestResponseDetailsDefault = not (bDownloadToFile or bSaveToFile);
    bShowRequest = bzShowRequest if fbIsProvided(bzShowRequest) else bShowRequestResponseDetailsDefault;
    bShowResponse = bzShowResponse if fbIsProvided(bzShowResponse) else bShowRequestResponseDetailsDefault;
    bShowDetails = bzShowDetails if fbIsProvided(bzShowDetails) else bShowRequestResponseDetailsDefault;
    
    if bSegmentedVideo and not bM3U:
      for rbSegmentedVideo in arbSegmentedVideos:
        obURLSegmentMatch = rbSegmentedVideo.match(oURL.sbAbsolute);
        if obURLSegmentMatch:
          break;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not identify segmentation from URL \"",
          COLOR_INFO, oURL.sbAbsolute,
          COLOR_NORMAL, "\"",
        );
        sys.exit(guExitCodeBadArgument);
      sbURLSegmentHeader, sbStartIndex, sbURLSegmentFooter = obURLSegmentMatch.groups();
      uStartIndex = int(sbStartIndex);
      if bShowProgress:
        oConsole.fOutput(
          COLOR_OK, CHAR_OK,
          COLOR_NORMAL, " Segmented URL: \"",
          COLOR_INFO, sbURLSegmentHeader,
          COLOR_HILITE, "*INDEX*",
          COLOR_INFO, sbURLSegmentFooter,
          COLOR_NORMAL, "\".",
        );
        oConsole.fOutput(
          COLOR_NORMAL, "  Index will start at ",
          COLOR_HILITE, str(uStartIndex),
          COLOR_NORMAL, ".",
        );
    ### COOKIE STORE ##########################################################
    bSaveCookiesToDisk = fbIsProvided(s0zCookieStoreJSONPath);
    if bSaveCookiesToDisk:
      s0zCookieStoreJSONPath  = s0zCookieStoreJSONPath or "HTTPCookieStore.json";
      o0CookieStoreJSONFile = cFileSystemItem(s0zCookieStoreJSONPath);
      bCookieStoreFileExists = o0CookieStoreJSONFile.fbIsFile();
      def fSaveCookiesToDiskAndOutputSetCookie(oCookieStore, oCookie, o0PreviousCookie):
        dxJSON = oCookieStore.fdxExportToJSON();
        sbJSON = bytes(json.dumps(dxJSON), "ascii", "strict");
        if bShowProgress:
          oConsole.fStatus(
            "      ",
            COLOR_BUSY, CHAR_BUSY,
            COLOR_NORMAL, " Saving cookie store to file ",
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
            COLOR_NORMAL, "...",
          );
        try:
          o0CookieStoreJSONFile.fbWrite(sbJSON, bThrowErrors = True);
        except Exception as oException:
          oConsole.fStatus();
          oConsole.fOutput(
            "      ",
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Could not write cookie store file ",
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
            COLOR_NORMAL, "!",
          );
          fOutputExceptionAndExit(oException, guExitCodeCannotWriteCookiesToFile);
        oConsole.fStatus();
        fOutputSetCookie(oCookieStore, oCookie, o0PreviousCookie);
    else:
      bCookieStoreFileExists = False;
    oCookieStore = cHTTPCookieStore(
      f0InvalidCookieAttributeCallback = fOutputInvalidCookieAttributeAndExit,
      f0SetCookieCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookiesToDisk else fOutputSetCookie,
      f0CookieExpiredCallback = fSaveCookiesToDiskAndOutputSetCookie if bSaveCookiesToDisk else fOutputSetCookie,
      f0CookieAppliedCallback = None, # (oRequest, oURL, oCookie)
      f0HeaderAppliedCallback = None, # (oRequest, oURL, oHeader)
      f0CookieReceivedCallback = None, # (oResponse, oURL, oCookie)
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
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
            COLOR_NORMAL, "...",
          );
        try:
          sbCookieStoreJSON = o0CookieStoreJSONFile.fsbRead();
        except Exception as oException:
          oConsole.fOutput(
            "      ",
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Could not read cookie store file ",
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
            COLOR_NORMAL, ".",
          );
          fOutputExceptionAndExit(oException, guExitCodeCannotReadCookiesFromFile);
        if bShowProgress:
          oConsole.fStatus(
            "      ",
            COLOR_BUSY, CHAR_BUSY,
            COLOR_NORMAL, " Parsing cookie store file ",
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
            COLOR_NORMAL, "...",
          );
        try:
          dxCookieStoreJSON = json.loads(str(sbCookieStoreJSON, "ascii", "strict"));
        except ValueError as oException:
          oConsole.fOutput(
            "      ",
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Could not parse cookie store file ",
            COLOR_INFO, o0CookieStoreJSONFile.sPath,
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
        not o0CookieStoreJSONFile.o0Parent
        or not o0CookieStoreJSONFile.o0Parent.fbIsFolder()
      ):
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not find cookie store file ",
          COLOR_INFO, o0CookieStoreJSONFile.sPath,
          COLOR_NORMAL, " or the folder in which it is located.",
        );
        sys.exit(guExitCodeBadArgument);
    else:
      o0CookieStoreJSONFile = None;
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
        bVerifyCertificates = bVerifyCertificates,
      );
      # Create event handlers specific to this situation that call the generic request/response reporters
      if bShowProgress:
        oClient.fAddCallbacks({
          "request sent": lambda oClient, oConnection, oRequest:
              fHandleRequestSent(oConnection, oRequest, None, False), # None, False => no proxy, no need to show CONNECT requests
          "request sent and response received": lambda oClient, oConnection, oRequest, oResponse:
            fHandleRequestSentAndResponseReceived(oConnection, oRequest, oResponse, None, False), # None, False => no proxy, no need to show CONNECT responses
        });
      if bShowRequest:
        oClient.fAddCallback("request sent", lambda oClient, oConnection, oRequest:
          fOutputRequestSent(oRequest, bShowDetails, bDecodeBody, xPrefix = "")
        );
      if bShowResponse:
        # If we do this with "response received" event, it will fire before we have shown progress (above)
        oClient.fAddCallback("request sent and response received", lambda oClient, oConnection, oRequest, oResponse:
          fOutputResponseReceived(oResponse, bShowDetails, bDecodeBody, xPrefix = "")
        );
    elif o0HTTPProxyServerURL:
      # Create a HTTP client instance that uses a static proxy
      oClient = cHTTPClientUsingProxyServer(
        o0HTTPProxyServerURL, 
        o0CookieStore = oCookieStore,
        bVerifyCertificates = bVerifyCertificates,
      );
      # Create event handlers specific to this situation that call the generic request/response reporters
      if bShowProgress:
        oClient.fAddCallbacks({
          "request sent": lambda oClient, oConnection, oRequest:
              fHandleRequestSent(oConnection, oRequest, o0HTTPProxyServerURL, bShowProxyConnects), 
          "request sent and response received": lambda oClient, oConnection, oRequest, oResponse:
              fHandleRequestSentAndResponseReceived(oConnection, oRequest, oResponse, o0HTTPProxyServerURL, bShowProxyConnects),
        });
      if bShowRequest:
        oClient.fAddCallback("request sent", lambda oClient, oConnection, oRequest: 
          fOutputRequestSent(oRequest, bShowDetails, bDecodeBody, xPrefix = "")
        );
      if bShowResponse:
        # If we do this with "response received" event, it will fire before we have shown progress (above)
        oClient.fAddCallback("request sent and response received", lambda oClient, oConnection, oRequest, oResponse:
          fOutputResponseReceived(oResponse, bShowDetails, bDecodeBody, xPrefix = "")
        );
    else:
      # Create a HTTP client instance that uses dynamic proxies.
      oClient = cHTTPClientUsingAutomaticProxyServer(
        o0CookieStore = oCookieStore,
        bVerifyCertificates = bVerifyCertificates,
      );
      if bShowProgress:
        oClient.fAddCallbacks({
          "request sent": lambda oClient, oSecondaryClient, o0ProxyServerURL, oConnection, oRequest:
              fHandleRequestSent(oConnection, oRequest, o0HTTPProxyServerURL, bShowProxyConnects), 
          "request sent and response received": lambda oClient, oSecondaryClient, o0ProxyServerURL, oConnection, oRequest, oResponse:
              fHandleRequestSentAndResponseReceived(oConnection, oRequest, oResponse, o0HTTPProxyServerURL, bShowProxyConnects),
        });
      if bShowRequest:
        oClient.fAddCallback("request sent", lambda oClient, oSecondaryClient, o0ProxyServerURL, oConnection, oRequest:
          fOutputRequestSent(oRequest, bShowDetails, bDecodeBody, xPrefix = "")
        );
      if bShowResponse:
        # If we do this with "response received" event, it will fire before we have shown progress (above)
        oClient.fAddCallback("request sent and response received", lambda oClient, oSecondaryClient, o0ProxyServerURL, oConnection, oRequest, oResponse:
          fOutputResponseReceived(oResponse, bShowDetails, bDecodeBody, xPrefix = "")
        );
    if bShowProgress:
      if isinstance(oClient, (cHTTPClient, cHTTPClientUsingAutomaticProxyServer)):
        oClient.fAddCallbacks({
          "server hostname or ip address invalid": fHandleServerHostnameOrIPAddressInvalid,
          
          "resolving server hostname": fHandleResolvingServerHostname,
          "resolving server hostname failed": fHandleResolvingServerHostnameFailed,
          "server hostname resolved to ip address": fHandleServerHostnameResolvedToIPAddress,
          
          "connecting to server ip address": fHandleConnectingToServerIPAddress,
          "connecting to server ip address failed": fHandleConnectingToServerIPAddressFailed,
          # We will always inform the user of this
          # "connecting to server failed": fHandleConnectingToServerFailed,
          "connection to server created": fHandleConnectionToServerCreated,
          "connection to server terminated": fHandleConnectionToServerTerminated,
        });
      if isinstance(oClient, (cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer)):
        oClient.fAddCallbacks({
          "proxy hostname or ip address invalid": fHandleProxyHostnameOrIPAddressInvalid,
          "resolving proxy hostname": fHandleResolvingProxyHostname,
          "resolving proxy hostname failed": fHandleResolvingProxyHostnameFailed,
          "proxy hostname resolved to ip address": fHandleProxyHostnameResolvedToIPAddress,
          
          "connecting to proxy ip address": fHandleConnectingToProxyIPAddress,
          "connecting to proxy ip address failed": fHandleConnectingToProxyIPAddressFailed,
          # We will always inform the user of this
          # "connecting to server failed": fHandleConnectingToServerFailed,
          "connection to proxy created": fHandleConnectionToProxyCreated,
          "connection to proxy terminated": fHandleConnectionToProxyTerminated,
          "secure connection to server through proxy created": fHandleSecureConnectionToServerThroughProxyCreated,
          "secure connection to server through proxy terminated": fHandleSecureConnectionToServerThroughProxyTerminated,
        });
    
    ### M3U ######################################################################
    if bM3U:
      oResponse = foGetResponseForURL(
        oHTTPClient = oClient,
        oURL = oURL,
        sbzHTTPVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        s0RequestData = s0RequestData,
        dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
        d0Form_sValue_by_sName = d0Form_sValue_by_sName,
        u0MaxRedirects = u0MaxRedirects,
        bDownloadToFile = False,
        bSaveToFile = False,
        s0TargetFilePath = None,
        bIsFirstDownload = True,
        bShowProgress = bShowProgress,
      );
      if oResponse.uStatusCode != 200:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot download M3U file.",
        );
        sys.exit(guExitCodeNoValidResponseReceived);
      s0M3UContents = oResponse.fs0GetData();
      if s0M3UContents is None:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Provided URL does not contain an M3U file.",
        );
        sys.exit(guExitCodeNoValidResponseReceived);
      aoURLs = faoGetURLsFromM3U(s0M3UContents, oURL);
      if not aoURLs:
        oConsole.fOutput(
          "      ",
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Provided M3U file URL does not contain any links.",
        );
        sys.exit(guExitCodeNoValidResponseReceived);
      uProcessedURLs = 0;
      uDownloadedURLs = 0;
      if bSegmentedVideo:
        asPathSegments = oURL.asURLDecodedPath;
        if asPathSegments:
          s0TargetFilePath = asPathSegments[-1] + ".mp4";
        else:
          s0TargetFilePath = "video.mp4";
      for oURL in aoURLs:
        oResponse = foGetResponseForURL(
          oHTTPClient = oClient,
          oURL = oURL,
          sbzHTTPVersion = sbzHTTPVersion,
          sbzMethod = sbzMethod,
          s0RequestData = s0RequestData,
          dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName = d0Form_sValue_by_sName,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bIsFirstDownload = uProcessedURLs == 0 if bSegmentedVideo else True,
          bShowProgress = bShowProgress,
        );
        if oResponse.uStatusCode != 200 and bDownloadToFile:
          # We are missing a piece of the video, stop.
          break;
        else:
          uDownloadedURLs += 1;
        uProcessedURLs += 1;

      oConsole.fOutput(
        "      ",
        [COLOR_ERROR, CHAR_ERROR] if uDownloadedURLs == 0 else
            [COLOR_WARNING, CHAR_WARNING] if uDownloadedURLs != uProcessedURLs else
            [COLOR_OK, CHAR_OK],
        COLOR_NORMAL, [" Unable to downloaded any "] if uProcessedURLs == 0 else
            [
              " Downloaded all ",
              COLOR_INFO, str(uDownloadedURLs),
            ] if uProcessedURLs == uDownloadedURLs else [
              " Downloaded ",
              COLOR_INFO, str(uDownloadedURLs),
              COLOR_NORMAL, "/",
              COLOR_INFO, str(uProcessedURLs),
            ],
        COLOR_NORMAL, " ",
            ["segments"] if bDownloadToFile else ["files"],
        COLOR_NORMAL, ".",
      );
    elif bSegmentedVideo:
      # Multiple request to URL with increasing index until we get a response that is not "200 COLOR_OK"
      uIndex = uStartIndex;
      while 1:
        oURL = cURL.foFromBytesString(b"%s%d%s" % (sbURLSegmentHeader, uIndex, sbURLSegmentFooter));
        oResponse = foGetResponseForURL(
          oHTTPClient = oClient,
          oURL = oURL,
          sbzHTTPVersion = sbzHTTPVersion,
          sbzMethod = sbzMethod,
          s0RequestData = s0RequestData,
          dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName = d0Form_sValue_by_sName,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bIsFirstDownload = uIndex == uStartIndex,
          bShowProgress = bShowProgress,
        );
        if oResponse.uStatusCode != 200:
          break;
        uIndex += 1;
      if bShowProgress:
        oConsole.fOutput(
          "      ",
          COLOR_OK, CHAR_OK,
          COLOR_NORMAL, " Found ",
          COLOR_INFO, str(uIndex - uStartIndex),
          COLOR_NORMAL, " segments.",
        );
    else:
      # Single request
      foGetResponseForURL(
        oHTTPClient = oClient,
        oURL = oURL,
        sbzHTTPVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        s0RequestData = s0RequestData,
        dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
        d0Form_sValue_by_sName = d0Form_sValue_by_sName,
        u0MaxRedirects = u0MaxRedirects,
        bDownloadToFile = bDownloadToFile,
        bSaveToFile = bSaveToFile,
        s0TargetFilePath = s0TargetFilePath,
        bIsFirstDownload = True,
        bShowProgress = bShowProgress,
      );
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;