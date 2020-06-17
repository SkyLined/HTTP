from fCheckDependencies import fCheckDependencies;
fCheckDependencies();

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
  import re, sys;
  
  from oConsole import oConsole;
  from cFileSystemItem import cFileSystemItem;
  from mHTTP import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPHeaders, cURL;
  
  from mColors import *;
  from fPrintUsageInformation import fPrintUsageInformation;
  from fPrintVersionInformation import fPrintVersionInformation;

  rURL = re.compile(r"^https?://.*$", re.I);
  rMethod = re.compile(r"^[A-Z]+$", re.I);
  rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
  rSegmentedVideo = re.compile(
    "("
      r".*\b"
      r"[\w\-]+"
    ")("
      r"\d+"
    ")("
      r"(?:\-\w+)*"
      r"\.ts"
      r"(?:\?.*)?"
    ")"
  );

  def fOutputResponseStatusLine(oResponse):
    if 100 <= oResponse.uStatusCode < 200: 
      xColor = HTTP_STATUS_LINE_1xx;
    elif 200 <= oResponse.uStatusCode < 300: 
      xColor = HTTP_STATUS_LINE_2xx;
    elif 300 <= oResponse.uStatusCode < 400: 
      xColor = HTTP_STATUS_LINE_3xx;
    elif 400 <= oResponse.uStatusCode < 500: 
      xColor = HTTP_STATUS_LINE_4xx;
    elif 500 <= oResponse.uStatusCode < 600: 
      xColor = HTTP_STATUS_LINE_5xx;
    else:
      xColor = HTTP_STATUS_LINE_INVALID;
    oConsole.fOutput(xColor, oResponse.fsGetStatusLine());

  
  asArguments = sys.argv[1:];
  dsAdditionalHeaders = {};
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
      elif sName == ["-dc", "--decode-body"]:
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
        assert len(tsHeader) == 2, \
            "Headers must be of the form name:value";
        sName, sValue = tsHeader;
        dsAdditionalHeaders[sName] = sValue;
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
    oURLSegmentMatch = rSegmentedVideo.match(sURL);
    assert oURLSegmentMatch, \
        "Could not identify segmentation from URL %s!" % sURL;
    sURLSegmentHeader, sIndex, sURLSegmentFooter = oURLSegmentMatch.groups();
    uIndex = long(sIndex);
  sMethod = szMethod or "GET";
  sHTTPVersion = szHTTPVersion or "HTTP/1.1";
  oHTTPClient = (
    cHTTPClientUsingProxyServer(oHTTPProxyServerURL) if oHTTPProxyServerURL else
    cHTTPClient()
  );
  oHTTPHeaders = cHTTPHeaders.foDefaultHeadersForVersion(sHTTPVersion);
  for (sName, sValue) in dsAdditionalHeaders.items():
    oHTTPHeaders.fbReplaceHeadersForName(sName, sValue);
  asRedirectedFromURLs = [];
  bFirstDownload = True;
  oURL = None;
  while 1:
    if oURL is None:
      if bSegmentedVideo:
        sCurrentURL = "%s%d%s" % (sURLSegmentHeader, uIndex, sURLSegmentFooter);
        oURL = cURL.foFromString(sCurrentURL);
        assert oURL, \
            "Invalid URL %s" % sCurrentURL;
      else:
        oURL = cURL.foFromString(sURL);
        assert oURL, \
            "Invalid URL %s" % sURL;
    oConsole.fStatus(INFO, sHTTPVersion, " ", sMethod, " ", str(oURL), NORMAL, "...");
    oRequest, oResponse = oHTTPClient.ftoGetRequestAndResponseForURL(
      oURL = oURL,
      szVersion = sHTTPVersion,
      szMethod = sMethod,
      ozHeaders = oHTTPHeaders,
      szData = szRequestData,
    );
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
            oConsole.fOutput(HTTP_HEADER_NAME, "Location", NORMAL, ": ", HTTP_HEADER_VALUE, str(oURL));
            continue;
          else:
            oConsole.fOutput(ERROR, "- Redirected to invalid URL ", ERROR_INFO, repr(sRedirectToURL), ERROR, ".");
        else:
          oConsole.fOutput(ERROR, "- Redirected without providing a ", ERROR_INFO, "Location", ERROR, " header.");
    sResponseData = oResponse.sData;
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
      oConsole.fOutput(HTTP_REQUEST_STATUS_LINE, oRequest.fsGetStatusLine());
      # Output request headers
      for oHTTPHeader in oRequest.oHeaders.faoGetHeaders():
        asValueLines = oHTTPHeader.asValueLines;
        oConsole.fOutput(HTTP_HEADER_NAME, oHTTPHeader.sName, NORMAL, ": ", HTTP_HEADER_VALUE, asValueLines[0]);
        for sValueLine in asValueLines[1:]:
          oConsole.fOutput(HTTP_HEADER_VALUE, sValueLine);
      if oRequest.sBody:
        # Output request body
        oConsole.fOutput(HTTP_BODY, oRequest.sBody);
      # Output separator
      oConsole.fOutput(sPadding = "-");
      # Output response status line
      fOutputResponseStatusLine(oResponse);
      # Output response headers
      for oHTTPHeader in oResponse.oHeaders.faoGetHeaders():
        asValueLines = oHTTPHeader.asValueLines;
        oConsole.fOutput(HTTP_HEADER_NAME, oHTTPHeader.sName, NORMAL, ": ", HTTP_HEADER_VALUE, asValueLines[0]);
        for sValueLine in asValueLines[1:]:
          oConsole.fOutput(HTTP_HEADER_VALUE, sValueLine);
      # Output response body
      if bDecodeBody:
        if sResponseData:
          oConsole.fOutput(HTTP_BODY_DECODED, unicode(sResponseData));
      elif oResponse.sBody:
        oConsole.fOutput(HTTP_BODY, oResponse.sBody);
      if oRequest.ozAdditionalHeaders:
        # Output response additional headers
        for oHTTPHeader in oRequest.ozAdditionalHeaders.faoGetHeaders():
          asValueLines = oHTTPHeader.asValueLines;
          oConsole.fOutput(HTTP_HEADER_NAME, oHTTPHeader.sName, NORMAL, ": ", HTTP_HEADER_VALUE, asValueLines[0]);
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