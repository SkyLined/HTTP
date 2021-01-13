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

CR_CHAR = u"\u2190";
LF_CHAR = u"\u2193";
CRLF_CHAR = u"\u2190\u2518";
EOF_CHAR = u"\u25A0";

try:
  import re, sys;
  
  from oConsole import oConsole;
  from cFileSystemItem import cFileSystemItem;
  from mHTTP import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPHeaders, cURL, mExceptions;
  
  from mColors import *;
  from fPrintUsageInformation import fPrintUsageInformation;
  from fPrintVersionInformation import fPrintVersionInformation;
  
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
  
  def fOutputResponseStatusLine(oResponse):
    if 100 <= oResponse.uStatusCode < 200: 
      xColor = HTTP_RESPONSE_STATUS_LINE_1xx;
    elif 200 <= oResponse.uStatusCode < 300: 
      xColor = HTTP_RESPONSE_STATUS_LINE_2xx;
    elif 300 <= oResponse.uStatusCode < 400: 
      xColor = HTTP_RESPONSE_STATUS_LINE_3xx;
    elif 400 <= oResponse.uStatusCode < 500: 
      xColor = HTTP_RESPONSE_STATUS_LINE_4xx;
    elif 500 <= oResponse.uStatusCode < 600: 
      xColor = HTTP_RESPONSE_STATUS_LINE_5xx;
    else:
      xColor = HTTP_RESPONSE_STATUS_LINE_INVALID;
    oConsole.fOutput(
      xColor, oResponse.fsGetStatusLine(),
      HTTP_CRLF, CRLF_CHAR
    );
  
  def fOutputBodyLines(xColor, asBodyLines):
    for sBodyLine in asBodyLines[:-1]:
      # "" -> [""], "A" -> ["A"], "A\r" -> ["A", ""], "A\rB" -> ["A", "B"]
      asBodyLineChunks = sBodyLine.split("\r");
      bBodyLineEndsWithCRLF = len(asBodyLineChunks) > 1 and asBodyLineChunks[-1] == "";
      if bBodyLineEndsWithCRLF:
        asBodyLineChunks.pop();
      # "" -> [""]/F, "A" -> ["A"]/F, "A\r" -> ["A"]/T, "A\rB" -> ["A", "B"]/F
      for sBodyLineChunks in asBodyLineChunks[:-1]:
        oConsole.fOutput(xColor, sBodyLineChunks, HTTP_CRLF, CR_CHAR);
      sLastBodyLineChunk = asBodyLineChunks[-1];
      # "" -> ""/F, "A" -> "A"/F, "A\r" -> "A"/T, "A\rB" -> "B"/F
      oConsole.fOutput(xColor, sLastBodyLineChunk, HTTP_CRLF, CRLF_CHAR if bBodyLineEndsWithCRLF else LF_CHAR);
    if asBodyLines:
      sLastBodyLine = asBodyLines[-1];
      asLastBodyLineChunks = sLastBodyLine.split("\r") if sLastBodyLine else [];
      # "" -> [], "A" -> ["A"], "A\r" -> ["A", ""], "A\rB" -> ["A", "B"]
      bLastBodyLineEndsWithCRLF = len(asLastBodyLineChunks) > 1 and asLastBodyLineChunks[-1] == "";
      if bLastBodyLineEndsWithCRLF:
        asLastBodyLineChunks.pop();
      for sBodyLineChunks in asLastBodyLineChunks[:-1]:
        oConsole.fOutput(xColor, sBodyLineChunks, HTTP_CRLF, CR_CHAR);
      if asLastBodyLineChunks:
        sLastBodyLineLastChunk = asLastBodyLineChunks[-1];
        oConsole.fOutput(xColor, sLastBodyLineLastChunk, HTTP_CRLF, EOF_CHAR);
  
  asArguments = sys.argv[1:];
  dsAdditionalOrRemovedHeaders = {};
  szMethod = None;
  sURL = None;
  bSegmentedVideo = None;
  uIndex = None;
  szHTTPVersion = None;
  oHTTPProxyServerURL = None;
  szRequestData = None;
  bDecodeBody = False;
  bDownload = False;
  bFollowRedirects = False;
  bAllowUnverifiableCertificates = False;
  sDownloadToFilePath = None;
  for sArgument in asArguments:
    if sArgument.startswith("-"):
      sName, sValuePlusEqualsSign = (sArgument + "=").split("=", 1);
      assert sName, \
          "Invalid argument %s!" % sArgument;
      sValue = sValuePlusEqualsSign[:-1];
      if sName in ["-?", "-h", "--help", "/?", "/h", "/help"]:
        fPrintUsageInformation();
        sys.exit(0);
      elif sName in ["--version", "/version"]:
        fPrintVersionInformation(
          bCheckForUpdates = True,
          bCheckAndShowLicenses = True,
          bShowInstallationFolders = True,
        );
        sys.exit(0);
      elif sName in ["--debug"]:
        assert not sValue, \
            "--%s argument does not accept a value!" % sName;
        from mDebugOutput import fEnableAllDebugOutput;
        fEnableAllDebugOutput();
      elif sName in ["--data"]:
        szRequestData = sValue;
      elif sName in ["--data-file"]:
        oDataFileSystemItem = cFileSystemItem(sValue);
        assert sValue and oDataFileSystemItem.fbIsFile(bParseZipFiles = True), \
            "%s argument requires a valid file path as a value!" % sName;
        szRequestData = oDataFileSystemItem.fsRead(bParseZipFiles = True);
      elif sName in ["--unsecure", "--unsecured", "--insecure"]:
        bAllowUnverifiableCertificates = True;
      elif sName in ["-dl", "--download"]:
        assert not bDecodeBody, \
            "The --decode-body is superfluous when the --download argument is provided";
        bDownload = True;
        if sValue:
          assert sDownloadToFilePath in [None, sValue], \
              "You cannot provide more than one file path to download to.";
          sDownloadToFilePath = sValue;
      elif sName in ["-sv", "--segmented-video"]:
        assert not bDecodeBody, \
            "The --decode-body is superfluous when the --segmented-video argument is provided";
        bDownload = True;
        bFollowRedirects = True;
        bSegmentedVideo = True;
        if sValue:
          assert sDownloadToFilePath in [None, sValue], \
              "You cannot provide more than one file path to download to.";
          sDownloadToFilePath = sValue;
      elif sName in ["-r", "--follow-redirects"]:
        assert not sValue, \
            "--%s argument does not accept a value!" % sName;
        bFollowRedirects = True;
      elif sName in ["-db", "--decode-body"]:
        assert not sValue, \
            "--%s argument does not accept a value!" % sName;
        bDecodeBody = True;
        assert not bDownload, \
            "The --decode-body is superfluous when the --download argument is provided";
        assert not bSegmentedVideo, \
            "The --decode-body is superfluous when the --segmented-video argument is provided";
      elif sName in ["-p", "--http-proxy"]:
        assert sValue, \
            "--%s argument requires a value!" % sName;
        oHTTPProxyServerURL = cURL.foFromString(sValue);
        assert oHTTPProxyServerURL, \
            "Invalid argument %s: value is not a valid URL!" % sArgument;
      elif sName in ["--header"]:
        tsHeader = sValue.split(":", 1);
        if len(tsHeader) == 1:
          sHeaderName = sValue; sHeaderValue = None;
        else:
          assert len(tsHeader) == 2, \
              "Headers must be of the form name:value";
          sHeaderName, sHeaderValue = tsHeader;
          if sHeaderValue.strip() == "":
            sHeaderValue = None;
        dsAdditionalOrRemovedHeaders[sHeaderName] = sHeaderValue;
      else:
        assert False, \
            "Unknown argument %s" % sArgument;
    elif sURL is None and rURL.match(sArgument):
      sURL = sArgument;
    elif szMethod is None and rMethod.match(sArgument):
      szMethod = sArgument;
    elif szHTTPVersion is None and rHTTPVersion.match(sArgument):
      szHTTPVersion = sArgument;
    else:
      assert False, \
          "Superfluous argument %s" % sArgument;
  if sURL is None:
    fPrintUsageInformation();
    sys.exit(0);
  if bSegmentedVideo:
    for rSegmentedVideo in arSegmentedVideos:
      oURLSegmentMatch = rSegmentedVideo.match(sURL);
      if oURLSegmentMatch:
        break;
    else:
      raise AssertionError("Could not identify segmentation from URL %s!" % sURL);
    sURLSegmentHeader, sIndex, sURLSegmentFooter = oURLSegmentMatch.groups();
    uIndex = long(sIndex);
    oConsole.fOutput(NORMAL, "+ Segmented URL: ", sURLSegmentHeader, INFO, "*INDEX*", NORMAL, sURLSegmentFooter);
    oConsole.fOutput(NORMAL, "  Starting at index ", INFO, str(uIndex), NORMAL, ".");
  sMethod = szMethod or "GET";
  sHTTPVersion = szHTTPVersion or "HTTP/1.1";
  oHTTPClient = (
    cHTTPClientUsingProxyServer(oHTTPProxyServerURL, bAllowUnverifiableCertificates = bAllowUnverifiableCertificates)
    if oHTTPProxyServerURL else
    cHTTPClient(bAllowUnverifiableCertificates = bAllowUnverifiableCertificates)
  );
  oHTTPHeaders = cHTTPHeaders.foDefaultHeadersForVersion(sHTTPVersion);
  for (sName, sValue) in dsAdditionalOrRemovedHeaders.items():
    if sValue is None:
      oHTTPHeaders.fbRemoveHeadersForName(sName);
    else:
      oHTTPHeaders.fbReplaceHeadersForName(sName, sValue);
  asRedirectedFromURLs = [];
  bFirstDownload = True;
  oURL = None;
  while 1:
    if oURL is None:
      try:
        if bSegmentedVideo:
          sCurrentURL = "%s%d%s" % (sURLSegmentHeader, uIndex, sURLSegmentFooter);
          oURL = cURL.foFromString(sCurrentURL);
          assert oURL, \
              "Invalid URL %s" % sCurrentURL;
        else:
          oURL = cURL.foFromString(sURL);
          assert oURL, \
              "Invalid URL %s" % sURL;
      except mExceptions.cInvalidURLException as oException:
        oConsole.fOutput(ERROR, "- Invalid URL:");
        oConsole.fOutput(ERROR, "  ", ERROR_INFO, oException.sMessage);
        sys.exit(1);
    
    oConsole.fStatus(INFO, sHTTPVersion, " ", sMethod, " ", str(oURL), NORMAL, "...");
    try:
      oRequest, ozResponse = oHTTPClient.ftozGetRequestAndResponseForURL(
        oURL = oURL,
        szVersion = sHTTPVersion,
        szMethod = sMethod,
        ozHeaders = oHTTPHeaders,
        szData = szRequestData,
      );
    except Exception as oException:
      bSSLSupportEnabled = hasattr(mExceptions, "cSSLException");
      if isinstance(oException, mExceptions.cTCPIPConnectTimeoutException):
        oConsole.fOutput(ERROR, "- Connecting to server timed out:");
      elif isinstance(oException, (
        mExceptions.cTCPIPConnectionRefusedException,
        mExceptions.cTCPIPInvalidAddressException,
        mExceptions.cDNSUnknownHostnameException,
      )):
        oConsole.fOutput(ERROR, "- Could not connect to server:");
      elif isinstance(oException, (
        mExceptions.cTCPIPConnectionDisconnectedException,
        mExceptions.cTCPIPConnectionShutdownException,
      )):
        oConsole.fOutput(ERROR, "- The server did not respond to our request:");
      elif isinstance(oException, mExceptions.cHTTPProxyConnectFailedException):
        oConsole.fOutput(ERROR, "- Could not connect to proxy server:");
      elif isinstance(oException, (
        mExceptions.cMaxConnectionsReachedException,
      )):
        oConsole.fOutput(ERROR, "- Could not connect to server:");
      elif isinstance(oException, (
        mExceptions.cMaxConnectionsReachedException,
      )):
        oConsole.fOutput(ERROR, "- Could not connect to server:");
      elif isinstance(oException, mExceptions.cTCPIPDataTimeoutException):
        oConsole.fOutput(ERROR, "- The server was unable to respond in a timely manner.");
      elif isinstance(oException, (
        mExceptions.cHTTPOutOfBandDataException,
        mExceptions.cHTTPInvalidMessageException,
      )):
        oConsole.fOutput(ERROR, "- There was a protocol error while talking to the server:");
      elif bSSLSupportEnabled and isinstance(oException, mExceptions.cSSLSecureTimeoutException):
        oConsole.fOutput(ERROR, "- Securing the connection to the server timed out:");
      elif bSSLSupportEnabled and isinstance(oException, (
        mExceptions.cSSLWrapSocketException,
        mExceptions.cSSLSecureHandshakeException,
        mExceptions.cSSLCannotGetRemoteCertificateException,
        mExceptions.cSSLIncorrectHostnameException,
      )):
        oConsole.fOutput(ERROR, "- Securing the connection to the server failed:");
      else:
        raise;
      oConsole.fOutput(ERROR, "  ", ERROR_INFO, oException.sMessage);
      sys.exit(1);
    assert ozResponse, \
        "Expected a response, got %s" % ozResponse;
    oResponse = ozResponse;
    if bFollowRedirects and oResponse.uStatusCode in [301, 302, 307, 308]:
      asRedirectedFromURLs.append(str(oURL));
      if len(asRedirectedFromURLs) >= 10:
        oConsole.fOutput(ERROR, "- Too many sequential redirects.");
        for sRedirectedFromURL in asRedirectedFromURLs:
          oConsole.fOutput(ERROR_INFO, "  ", sRedirectedFromURL);
      else:
        sRedirectToURL = oResponse.oHeaders.fsGet("Location");
        if sRedirectToURL:
          oURL = cURL.foFromString(sRedirectToURL);
          if oURL:
            fOutputResponseStatusLine(oResponse);
            oConsole.fOutput(
              HTTP_HEADER_NAME, "Location",
              NORMAL, ":",
              HTTP_HEADER_VALUE, str(oURL),
              HTTP_CRLF, CRLF_CHAR,
            );
            continue;
          else:
            oConsole.fOutput(ERROR, "- Redirected to invalid URL ", ERROR_INFO, repr(sRedirectToURL), ERROR, ".");
        else:
          oConsole.fOutput(ERROR, "- Redirected without providing a ", ERROR_INFO, "Location", ERROR, " header.");
    sResponseData = oResponse.szData or "";
    if bDownload and oResponse.uStatusCode == 200:
      if sDownloadToFilePath is None:
        sFilePath = oURL.asPath[-1];
        oDownloadToFile = cFileSystemItem(sFilePath);
      else:
        oDownloadToFile = cFileSystemItem(sDownloadToFilePath);
        if not bFirstDownload:
          oDownloadToFile.fbOpenAsFile(bWritable = True, bAppend = True);
      if not oDownloadToFile.fbWrite(sResponseData):
        oConsole.fOutput(
          ERROR, "- Cannot write ", ERROR_INFO, str(len(sResponseData)), ERROR, " bytes to ",
          ERROR_INFO, oDownloadToFile.sPath, ERROR, "."
        );
        break;
      if oDownloadToFile.fbIsOpenAsFile():
        oDownloadToFile.fbClose();
      oConsole.fOutput(
        "+ Saved ", INFO, str(len(sResponseData)), NORMAL, " bytes to ",
        INFO, oDownloadToFile.sPath, NORMAL, "."
      );
    elif bSegmentedVideo and oResponse.uStatusCode == 404:
      oConsole.fOutput("Found %d segments." % (uIndex - 1));
    else:
      # Output request status line
      oConsole.fOutput(
        HTTP_REQUEST_STATUS_LINE, oRequest.fsGetStatusLine(),
        HTTP_CRLF, CRLF_CHAR
      );
      # Output request headers
      for oHTTPHeader in oRequest.oHeaders.faoGetHeaders():
        asValueLines = oHTTPHeader.asValueLines;
        oConsole.fOutput(
          HTTP_HEADER_NAME, oHTTPHeader.sName,
          NORMAL, ":",
          HTTP_HEADER_VALUE, asValueLines[0],
          HTTP_CRLF, CRLF_CHAR
        );
        for sValueLine in asValueLines[1:]:
          oConsole.fOutput(
            HTTP_HEADER_VALUE, sValueLine,
            HTTP_CRLF, CRLF_CHAR
          );
      oConsole.fOutput(
        HTTP_CRLF, CRLF_CHAR, EOF_CHAR if not oRequest.sBody else ""
      );
      if oRequest.sBody:
        # Output request body
        fOutputBodyLines(HTTP_BODY, oRequest.sBody.split("\n"));
      # Output separator
      oConsole.fOutput(HTTP_REQUEST_RESPONSE_SEPARATOR, sPadding = u"\u2500");
      # Output response status line
      fOutputResponseStatusLine(oResponse);
      # Output response headers
      for oHTTPHeader in oResponse.oHeaders.faoGetHeaders():
        asValueLines = oHTTPHeader.asValueLines;
        oConsole.fOutput(
          HTTP_HEADER_NAME, oHTTPHeader.sName,
          NORMAL, ":",
          HTTP_HEADER_VALUE, asValueLines[0],
          HTTP_CRLF, CRLF_CHAR
        );
        for sValueLine in asValueLines[1:]:
          oConsole.fOutput(
            HTTP_HEADER_VALUE, sValueLine,
            HTTP_CRLF, CRLF_CHAR
          );
      # Output response body
      if oResponse.sBody:
        if bDecodeBody:
          asBodyLines = sResponseData.split("\n") if sResponseData else [];
          xColor = HTTP_BODY_DECODED;
        else:
          asBodyLines = oResponse.sBody.split("\n") if oResponse.sBody else [];
          xColor = HTTP_BODY;
        oConsole.fOutput(
          HTTP_CRLF, CRLF_CHAR, EOF_CHAR if not asBodyLines else ""
        );
        fOutputBodyLines(xColor, asBodyLines);
      if oRequest.ozAdditionalHeaders:
        # Output response additional headers
        for oHTTPHeader in oRequest.ozAdditionalHeaders.faoGetHeaders():
          asValueLines = oHTTPHeader.asValueLines;
          oConsole.fOutput(
            HTTP_HEADER_NAME, oHTTPHeader.sName,
            NORMAL, ": ",
            HTTP_HEADER_VALUE, asValueLines[0],
            HTTP_CRLF, CRLF_CHAR
          );
          for sValueLine in asValueLines[1:]:
            oConsole.fOutput(HTTP_HEADER_VALUE, sValueLine);
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