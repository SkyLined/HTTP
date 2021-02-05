import re, sys;

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  from mDebugOutput import *;
except: # Do nothing if not available.
  ShowDebugOutput = lambda fxFunction: fxFunction;
  fShowDebugOutput = lambda sMessage: None;
  fEnableDebugOutputForModule = lambda mModule: None;
  fEnableDebugOutputForClass = lambda cClass: None;
  fEnableAllDebugOutput = lambda: None;
  cCallStack = fTerminateWithException = fTerminateWithConsoleOutput = None;


try:
  from oConsole import oConsole;
  from cFileSystemItem import cFileSystemItem;
  from fsBytesToHumanReadableString import fsBytesToHumanReadableString;
  from mHTTP import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer, cHTTPHeaders, cURL, mExceptions;
  
  from fOutputRequest import fOutputRequest;
  from fOutputResponse import fOutputResponse;
  from fPrintUsageInformation import fPrintUsageInformation;
  from fPrintVersionInformation import fPrintVersionInformation;
  from mColors import *;
  
  rURL = re.compile(r"^https?://.*$", re.I);
  rMethod = re.compile(r"^[A-Z]+$", re.I);
  rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
  arSegmentedVideos = [re.compile(s) for s in [
    (
      "("
        r".*?/"
        r"(?:\w+\-)+?"
      ")("
        r"\d+"
      ")("
        r"(?:\-\w+)*"
        r"\.ts"
        r"(?:\?.*)?"
      ")"
    ), (
      "("
        r".*?/"
        r"(?:\w+\-)+?"
        r"(?:\w*?)"
      ")("
        r"\d+"
      ")("
        r"(?:\-\w+)*"
        r"\.ts"
        r"(?:\?.*)?"
      ")"
    )
  ]];
  
  def fExitWithError(*asMessages):
    oConsole.fOutput(ERROR, "- ", ERROR_INFO, str(asMessages[0]));
    for sMessage in asMessages[1:]:
      oConsole.fOutput("  ", ERROR, str(sMessage));
    sys.exit(1);
  
  asArguments = sys.argv[1:];
  dsAdditionalOrRemovedHeaders = {};
  szMethod = None;
  sURL = None;
  bSegmentedVideo = None;
  uIndex = None;
  szHTTPVersion = None;
  bShowProgress = True;
  bShowRequest = True;
  bShowResponse = True;
  bShowDetails = True;
  bUseProxy = False;
  o0HTTPProxyServerURL = None;
  s0RequestData = None;
  bDecodeBody = False;
  bDownload = False;
  bFollowRedirects = False;
  bAllowUnverifiableCertificates = False;
  sDownloadToFilePath = None;
  for sArgument in asArguments:
    if len(sArgument) >= 2 and sArgument.startswith("-") or sArgument.startswith("/"):
      sNameWithPrefix, sValuePlusEqualsSign = (sArgument + "=").split("=", 1);
      if sNameWithPrefix.startswith("--"):
        sLowerName = sNameWithPrefix[2:].lower();
      else:
        sLowerName = sNameWithPrefix[1:].lower();
      sValue = sValuePlusEqualsSign[:-1];
      if sLowerName in ["debug"]:
        if sValue:
          fExitWithError("%s argument does not accept a value!" % sNameWithPrefix);
        from mDebugOutput import fEnableAllDebugOutput;
        fEnableAllDebugOutput();
      elif sLowerName in ["data"]:
        s0RequestData = sValue;
      elif sLowerName in ["df", "data-file"]:
        oDataFileSystemItem = cFileSystemItem(sValue);
        if not sValue or not oDataFileSystemItem.fbIsFile(bParseZipFiles = True):
            fExitWithError("%s argument requires a valid file path as a value!" % sNameWithPrefix);
        s0zRequestData = oDataFileSystemItem.fsRead(bParseZipFiles = True);
      elif sLowerName in ["db", "decode", "decode-body"]:
        if sValue:
          fExitWithError("%s argument does not accept a value!" % sNameWithPrefix);
        bDecodeBody = True;
      elif sLowerName in ["dl", "download"]:
        bDownload = True;
        if sValue:
          if sDownloadToFilePath not in [None, sValue]:
            fExitWithError("You cannot provide more than one file path to download to.");
          sDownloadToFilePath = sValue;
      elif sLowerName in ["header"]:
        tsHeader = sValue.split(":", 1);
        if len(tsHeader) == 1:
          sHeaderName = sValue; sHeaderValue = None;
        else:
          sHeaderName, sHeaderValue = tsHeader;
          if sHeaderValue.strip() == "":
            sHeaderValue = None;
        dsAdditionalOrRemovedHeaders[sHeaderName] = sHeaderValue;
      elif sLowerName in ["?", "h", "help"]:
        fPrintUsageInformation();
        sys.exit(0);
      elif sLowerName in ["p", "proxy", "http-proxy"]:
        bUseProxy = True;
        if sValue:
          o0HTTPProxyServerURL = cURL.foFromString(sValue);
      elif sLowerName in ["r", "follow-redirects"]:
        if sValue:
          fExitWithError("%s argument does not accept a value!" % sNameWithPrefix);
        bFollowRedirects = True;
      elif sLowerName in ["sv", "segmented-video"]:
        bDownload = True;
        bFollowRedirects = True;
        bSegmentedVideo = True;
        if sValue:
          if sDownloadToFilePath not in [None, sValue]:
            fExitWithError("You cannot provide more than one file path to download to.");
          sDownloadToFilePath = sValue;
      elif sLowerName in ["u", "unsecure", "unsecured", "insecure"]:
        bAllowUnverifiableCertificates = True;
      elif sLowerName in ["no-progress"]:
        bShowProgress = False;
      elif sLowerName in ["no-request"]:
        bShowRequest = False;
      elif sLowerName in ["no-response"]:
        bShowResponse = False;
      elif sLowerName in ["no-details"]:
        bShowDetails = False;
      elif sLowerName in ["version"]:
        fPrintVersionInformation(
          bCheckForUpdates = True,
          bCheckAndShowLicenses = True,
          bShowInstallationFolders = True,
        );
        sys.exit(0);
      else:
        fExitWithError("Unknown argument \"%s\"" % sArgument);
    elif sURL is None and rURL.match(sArgument):
      sURL = sArgument;
    elif szMethod is None and rMethod.match(sArgument):
      szMethod = sArgument;
    elif szHTTPVersion is None and rHTTPVersion.match(sArgument):
      szHTTPVersion = sArgument;
    else:
      fExitWithError("Superfluous argument \"%s\"" % sArgument);
  if sURL is None:
    fPrintUsageInformation();
    sys.exit(0);
  if bSegmentedVideo:
    for rSegmentedVideo in arSegmentedVideos:
      oURLSegmentMatch = rSegmentedVideo.match(sURL);
      if oURLSegmentMatch:
        break;
    else:
      fExitWithError("Could not identify segmentation from URL %s!" % sURL);
    sURLSegmentHeader, sIndex, sURLSegmentFooter = oURLSegmentMatch.groups();
    uIndex = long(sIndex);
    if bShowProgress:
      oConsole.fOutput(NORMAL, "+ Segmented URL: ", INFO, sURLSegmentHeader, HILITE, "*INDEX*", INFO, sURLSegmentFooter);
      oConsole.fOutput(NORMAL, "  Starting at index ", HILITE, str(uIndex), HILITE, ".");
  sMethod = szMethod or "GET";
  sHTTPVersion = szHTTPVersion or "HTTP/1.1";
  
  def fReportRequestSent(oConnection, oRequest, o0ProxyServerURL):
    if bShowProgress:
      oConsole.fOutput(
        "+ ", HILITE, oRequest.fsGetStatusLine(), NORMAL, " request sent (",
        INFO, fsBytesToHumanReadableString(len(oRequest.fsSerialize())), NORMAL, ") ",
        ["through proxy server at ", INFO, str(o0ProxyServerURL), NORMAL] if o0ProxyServerURL else
            ["directly to server at ", INFO, str(oConnection.foGetURLForRemoteServer()), NORMAL],
        "."
      );
    if bShowRequest:
      fOutputRequest(oRequest, bShowDetails);
  def fReportResponseReceived(oConnection, oResponse, o0ProxyServerURL):
    if bShowProgress:
      oConsole.fOutput(
        "+ ", HILITE, oResponse.fsGetStatusLine(), NORMAL, " response received (",
        INFO, fsBytesToHumanReadableString(len(oResponse.fsSerialize())),
        [" ", oResponse.s0MediaType] if oResponse.s0MediaType else [], NORMAL, ") ",
        ["through proxy server at ", INFO, str(o0ProxyServerURL), NORMAL]
            if o0ProxyServerURL else
            ["directly from server at ", INFO, str(oConnection.foGetURLForRemoteServer()), NORMAL],
        "."
      );
    if bShowResponse:
      fOutputResponse(oResponse, bDecodeBody, bShowDetails);
  
  if not bUseProxy:
    # No proxy
    oHTTPClient = cHTTPClient(bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
    def fHandleRequestSent(oHTTPClient, oConnection, oRequest):
      fReportRequestSent(oConnection, oRequest, None);
    def fHandleResponseReceived(oHTTPClient, oConnection, oResponse):
      fReportResponseReceived(oConnection, oResponse, None);
  elif o0HTTPProxyServerURL:
    # Static proxy
    oHTTPClient = cHTTPClientUsingProxyServer(o0HTTPProxyServerURL, bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
    def fHandleRequestSent(oHTTPClient, oConnection, oRequest):
      fReportRequestSent(oConnection, oRequest, oHTTPClient.oProxyServerURL);
    def fHandleResponseReceived(oHTTPClient, oConnection, oResponse):
      fReportResponseReceived(oConnection, oResponse, oHTTPClient.oProxyServerURL);
  else:
    # Dynamic proxy
    oHTTPClient = cHTTPClientUsingAutomaticProxyServer(bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
    # The cHTTPClientUsingAutomaticProxyServer instance creates a single cHTTPClient instance to make direct requests and
    # one or more cHTTPClientUsingProxyServer instances to make requests through various proxies.
    # Whether or not a proxy was used for a request depends on what class oSecondaryHTTPClientUsingProxyServerOrNot is
    # in the event arguments.
    def fHandleRequestSent(oHTTPClient, oSecondaryHTTPClient, o0ProxyServerURL, oConnection, oRequest):
      fReportRequestSent(oConnection, oRequest, o0ProxyServerURL);
    def fHandleResponseReceived(oHTTPClient, oSecondaryHTTPClient, o0ProxyServerURL, oConnection, oResponse):
      fReportResponseReceived(oConnection, oResponse, o0ProxyServerURL);
  oHTTPClient.fAddCallback("request sent", fHandleRequestSent);
  oHTTPClient.fAddCallback("response received", fHandleResponseReceived);
  
  asRedirectedFromURLs = [];
  bFirstDownload = True;
  oURL = None;
  while 1:
    # Construct the (next) URL
    if oURL is None:
      try:
        if bSegmentedVideo:
          sCurrentURL = "%s%d%s" % (sURLSegmentHeader, uIndex, sURLSegmentFooter);
          oURL = cURL.foFromString(sCurrentURL);
        else:
          oURL = cURL.foFromString(sURL);
      except mExceptions.cInvalidURLException as oException:
        fExitWithError("Invalid URL %s: %s" % (sCurrentURL, oException.sMessage));
    # Construct the HTTP request
    oRequest = oHTTPClient.foGetRequestForURL(
      oURL = oURL,
      szVersion = sHTTPVersion,
      szMethod = sMethod,
      s0Data = s0RequestData,
    );
    for (sName, sValue) in dsAdditionalOrRemovedHeaders.items():
      if sValue is None:
        oRequest.oHTTPHeaders.fbRemoveHeadersForName(sName);
      else:
        oRequest.oHTTPHeaders.fbReplaceHeadersForName(sName, sValue);
    # Send the request and get the response.
    oConsole.fStatus(INFO, sHTTPVersion, " ", sMethod, " ", str(oURL), NORMAL, "...");
    try:
      o0Response = oHTTPClient.fo0GetResponseForRequestAndURL(oRequest, oURL);
    except Exception as oException:
      bSSLSupportEnabled = hasattr(mExceptions, "cSSLException");
      if isinstance(oException, mExceptions.cTCPIPConnectTimeoutException):
        sErrorMessage = "Connecting to server timed out:";
      elif isinstance(oException, (
        mExceptions.cTCPIPConnectionRefusedException,
        mExceptions.cTCPIPInvalidAddressException,
        mExceptions.cDNSUnknownHostnameException,
      )):
        sErrorMessage = "Could not connect to server:";
      elif isinstance(oException, (
        mExceptions.cTCPIPConnectionDisconnectedException,
        mExceptions.cTCPIPConnectionShutdownException,
      )):
        sErrorMessage = "The server did not respond to our request:";
      elif isinstance(oException, mExceptions.cHTTPProxyConnectFailedException):
        sErrorMessage = "Could not connect to proxy server:";
      elif isinstance(oException, (
        mExceptions.cMaxConnectionsReachedException,
      )):
        sErrorMessage = "Could not connect to server:";
      elif isinstance(oException, (
        mExceptions.cMaxConnectionsReachedException,
      )):
        sErrorMessage = "Could not connect to server:";
      elif isinstance(oException, mExceptions.cTCPIPDataTimeoutException):
        sErrorMessage = "The server was unable to respond in a timely manner.";
      elif isinstance(oException, (
        mExceptions.cHTTPOutOfBandDataException,
        mExceptions.cHTTPInvalidMessageException,
      )):
        sErrorMessage = "There was a protocol error while talking to the server:";
      elif bSSLSupportEnabled and isinstance(oException, mExceptions.cSSLSecureTimeoutException):
        sErrorMessage = "Securing the connection to the server timed out:";
      elif bSSLSupportEnabled and isinstance(oException, (
        mExceptions.cSSLWrapSocketException,
        mExceptions.cSSLSecureHandshakeException,
        mExceptions.cSSLCannotGetRemoteCertificateException,
        mExceptions.cSSLIncorrectHostnameException,
      )):
        sErrorMessage = "Securing the connection to the server failed:";
      else:
        raise;
      fExitWithError(sErrorMessage, oException.sMessage);
    if not o0Response:
      fExitWithError("No response received.");
    oResponse = o0Response;
    if bFollowRedirects and oResponse.uStatusCode in [301, 302, 307, 308]:
      asRedirectedFromURLs.append(str(oURL));
      if len(asRedirectedFromURLs) >= 10:
        fExitWithError("Too many sequential redirects:", *asRedirectedFromURLs);
      else:
        sRedirectToURL = oResponse.oHeaders.fsGet("Location");
        if sRedirectToURL:
          try:
            oURL = cURL.foFromString(sRedirectToURL);
          except mExceptions.cInvalidURLException as oException:
            fExitWithError("Redirect to invalid URL %s: %s" % (sCurrentURL, oException.sMessage));
          if bShowProgress:
            oConsole.fOutput(NORMAL, "+ Redirected to URL: ", INFO, str(oURL), NORMAL, ".");
          continue;
        else:
          fExitWithError("Redirected without a \"Location\" header.");
    if bDownload and oResponse.uStatusCode == 200:
      if sDownloadToFilePath is None:
        sFilePath = oURL.asPath[-1];
        oDownloadToFile = cFileSystemItem(sFilePath);
      else:
        oDownloadToFile = cFileSystemItem(sDownloadToFilePath);
        if not bFirstDownload:
          oDownloadToFile.fbOpenAsFile(bWritable = True, bAppend = True);
      sResponseData = oResponse.s0Data or "";
      if not oDownloadToFile.fbWrite(sResponseData):
        fExitWithError("Cannot write %s to %s." % (fsBytesToHumanReadableString(len(sResponseData)), oDownloadToFile.sPath));
      if oDownloadToFile.fbIsOpenAsFile():
        oDownloadToFile.fbClose();
      if bShowProgress:
        oConsole.fOutput(
          "+ Saved ", INFO, fsBytesToHumanReadableString(len(sResponseData)), NORMAL, " to ",
          INFO, oDownloadToFile.sPath, NORMAL, "."
        );
    elif bSegmentedVideo and oResponse.uStatusCode == 404:
      if bShowProgress:
        oConsole.fOutput("+ Found %d segments." % (uIndex - 1));
    if bSegmentedVideo and oResponse.uStatusCode == 200:
      asRedirectedFromURLs = [];
      uIndex += 1;
      bFirstDownload = False;
      oURL = None;
    else:
      break;
except Exception as oException:
  if fTerminateWithException:
    fTerminateWithException(oException);
  raise;