import re, sys;

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

try:
  from mConsole import oConsole;
  from mFileSystemItem import cFileSystemItem;
  from mHumanReadable import fsBytesToHumanReadableString;
  from mHTTPClient import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer, cHTTPHeaders, cURL, mExceptions;
  from mNotProvided import *;
  
  from fOutputRequest import fOutputRequest;
  from fOutputResponse import fOutputResponse;
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from mCP437 import fsCP437FromBytesString;
  from mColors import *;
  
  if __name__ == "__main__":
    oConsole.uDefaultColor =            NORMAL;
    oConsole.uDefaultBarColor =         BAR;
    oConsole.uDefaultProgressColor =    PROGRESS;
    
    rURL = re.compile(r"^https?://.*$", re.I);
    rMethod = re.compile(r"^[A-Z]+$", re.I);
    rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
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
    
    def fExitWithError(sMessage, o0Exception = None):
      oConsole.fOutput(ERROR, "- ", ERROR_INFO, sMessage);
      if o0Exception:
        oConsole.fOutput("  ", ERROR_INFO, str(o0Exception.sMessage));
        for (sName, xValue) in o0Exception.dxDetails.items():
          oConsole.fOutput("  ", ERROR, "\u2022 ", str(sName), " = ", ERROR_INFO, repr(xValue));
      sys.exit(1);
    
    asArguments = sys.argv[1:];
    dsbAdditionalOrRemovedHeaders = {};
    sbzMethod = zNotProvided;
    o0URL = None;
    bSegmentedVideo = None;
    uStartIndex = None;
    sbzHTTPVersion = zNotProvided;
    bShowProgress = True;
    bShowRequest = True;
    bShowResponse = True;
    bShowDetails = True;
    bUseProxy = False;
    o0HTTPProxyServerURL = None;
    s0RequestData = None;
    bDecodeBody = False;
    bDownload = False;
    uMaxRedirects = 0;
    bAllowUnverifiableCertificates = False;
    s0DownloadToFilePath = None;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      if s0LowerName in ["debug"]:
        if s0Value is None or s0Value.lower() == "true":
          if not m0DebugOutput:
            oConsole.fOutput(ERROR, "The ", ERROR_INFO, "mDebugOutput", ERROR, " module is needed to show debug information!");
            sys.exit(3);
          m0DebugOutput.fEnableAllDebugOutput();
        elif s0Value.lower() == "false":
          pass;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["data"]:
        if not s0Value:
          oConsole.fOutput(ERROR, "- You must provide a value for \"", ERROR_INFO, sArgument, ERROR, "\".");
          sys.exit(2);
        s0RequestData = s0Value;
      elif s0LowerName in ["df", "data-file"]:
        if not s0Value:
          oConsole.fOutput(ERROR, "- You must provide a value for \"", ERROR_INFO, sArgument, ERROR, "\".");
          sys.exit(2);
        oDataFileSystemItem = cFileSystemItem(s0Value);
        if not oDataFileSystemItem.fbIsFile(bParseZipFiles = True):
          oConsole.fOutput(ERROR, "- You must provide a path to an existing file as the value for \"", ERROR_INFO, sArgument, ERROR, "\".");
          sys.exit(2);
        try:
          sbRequestData = oDataFileSystemItem.fsbRead(bParseZipFiles = True, bThrowErrors = true);
          s0RequestData = str(sbRequestData, "utf-8", "strict");
        except Exception as oException:
          oConsole.fOutput(ERROR, "Cannot read from file ", ERROR_INFO, s0Value, ERROR, ":");
          oConsole.fOutput("  ", ERROR_INFO, str(oException.sMessage));
          for (sName, xValue) in oException.dxDetails.items():
            oConsole.fOutput("  ", ERROR, "\u2022 ", str(sName), " = ", ERROR_INFO, repr(xValue));
          sys.exit(5);
      elif s0LowerName in ["db", "decode", "decode-body"]:
        if s0Value is None or s0Value.lower() == "true":
          bDecodeBody = True;
        elif s0Value.lower() == "false":
          bDecodeBody = False;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["dl", "download"]:
        bDownload = True;
        if s0Value:
          if s0DownloadToFilePath is not None:
            oConsole.fOutput(ERROR, "- You can only provide a path to download to once.");
            sys.exit(2);
          s0DownloadToFilePath = s0Value;
      elif s0LowerName in ["header"]:
        if not s0Value:
          oConsole.fOutput(ERROR, "- You must provide a value for \"", ERROR_INFO, sArgument, ERROR, "\".");
          sys.exit(2);
        sbValue = bytes(ord(s) for s in s0Value);
        tsbHeader = sbValue.split(b":", 1);
        if len(tsbHeader) == 1:
          sbHeaderName = sbValue; sb0HeaderValue = None;
        else:
          sbHeaderName, sb0HeaderValue = tsbHeader;
          if sb0HeaderValue.strip() == "":
            sb0HeaderValue = None;
        dsbAdditionalOrRemovedHeaders[sbHeaderName] = sb0HeaderValue;
      elif s0LowerName in ["p", "proxy", "http-proxy"]:
        bUseProxy = True;
        if s0Value:
          if o0HTTPProxyServerURL is not None:
            oConsole.fOutput(ERROR, "- You can only provide a proxy URL once.");
            sys.exit(2);
          o0HTTPProxyServerURL = cURL.foFromBytesString(bytes(ord(s) for s in s0Value));
      elif s0LowerName in ["r", "max-redirects"]:
        try:
          uMaxRedirects = int(s0Value);
          assert uMaxRedirects >= 0, "";
        except:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be an ", ERROR_INFO, "integer larger than or equal to zero", ERROR, ".");
          sys.exit(2);
      elif s0LowerName in ["sv", "segmented-video"]:
        bDownload = True;
        bSegmentedVideo = True;
        if s0Value:
          if s0DownloadToFilePath is not None:
            oConsole.fOutput(ERROR, "- You can only provide a path to download to once.");
            sys.exit(2);
          s0DownloadToFilePath = s0Value;
      elif s0LowerName in ["s", "secure"]:
        if s0Value is None or s0Value.lower() == "true":
          bAllowUnverifiableCertificates = False;
        elif s0Value.lower() == "false":
          bAllowUnverifiableCertificates = True;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["show-progress"]:
        if s0Value is None or s0Value.lower() == "true":
          bShowProgress = True;
        elif s0Value.lower() == "false":
          bShowProgress = False;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["show-request"]:
        if s0Value is None or s0Value.lower() == "true":
          bShowRequest = True;
        elif s0Value.lower() == "false":
          bShowRequest = False;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["show-response"]:
        if s0Value is None or s0Value.lower() == "true":
          bShowResponse = True;
        elif s0Value.lower() == "false":
          bShowResponse = False;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName in ["show-details"]:
        if s0Value is None or s0Value.lower() == "true":
          bShowDetails = True;
        elif s0Value.lower() == "false":
          bShowDetails = False;
        else:
          oConsole.fOutput(ERROR, "- The value for ", ERROR_INFO, sArgument, ERROR, \
              " must be \"", ERROR_INFO, "true", ERROR, "\" (default) or \"", ERROR_INFO, "false", ERROR, "\".");
          sys.exit(2);
      elif s0LowerName:
        oConsole.fOutput(ERROR, "- Unknown argument ", ERROR_INFO, sArgument, ERROR, ".");
        sys.exit(2);
      elif o0URL is None and rURL.match(sArgument):
        o0URL = cURL.foFromBytesString(bytes(ord(s) for s in sArgument));
      elif not fbIsProvided(sbzMethod) and rMethod.match(sArgument):
        sbzMethod = bytes(ord(s) for s in sArgument);
      elif not fbIsProvided(sbzHTTPVersion) and rHTTPVersion.match(sArgument):
        sbzHTTPVersion = bytes(ord(s) for s in sArgument);
      else:
        oConsole.fOutput(ERROR, "- Superfluous argument ", ERROR_INFO, sArgument, ERROR, ".");
        sys.exit(2);
    if o0URL is None:
      fPrintUsageInformation();
      sys.exit(0);
    if bSegmentedVideo:
      for rbSegmentedVideo in arbSegmentedVideos:
        obURLSegmentMatch = rbSegmentedVideo.match(o0URL.sbAbsolute);
        if obURLSegmentMatch:
          break;
      else:
        oConsole.fOutput(ERROR, "Could not identify segmentation from URL ", ERROR_INFO, sURL);
        sys.exit(2);
      sbURLSegmentHeader, sbStartIndex, sbURLSegmentFooter = obURLSegmentMatch.groups();
      uStartIndex = int(sbStartIndex);
      if bShowProgress:
        oConsole.fOutput(NORMAL, "+ Segmented URL: ", INFO, sbURLSegmentHeader, HILITE, "*INDEX*", INFO, sbURLSegmentFooter);
        oConsole.fOutput(NORMAL, "  Starting at index ", HILITE, str(uStartIndex), HILITE, ".");
    
    def fReportRequestSent(oConnection, oRequest, o0ProxyServerURL):
      if bShowProgress:
        oConsole.fOutput(
          "+ ", HILITE, fsCP437FromBytesString(oRequest.fsbGetStatusLine()), NORMAL, " request (",
          INFO, fsBytesToHumanReadableString(len(oRequest.fsbSerialize())), NORMAL, ") sent ",
          [INFO, "securely "] if oConnection.bSecure else [WARNING, "in plain text "], NORMAL,
          ["through proxy server at ", INFO, fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute), NORMAL] if o0ProxyServerURL else
              ["to server at ", INFO, fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute), NORMAL],
          "."
        );
      if bShowRequest:
        fOutputRequest(oRequest, bDecodeBody, bShowDetails);
    def fReportResponseReceived(oConnection, oResponse, o0ProxyServerURL):
      if bShowProgress:
        oConsole.fOutput(
          "+ ", HILITE, fsCP437FromBytesString(oResponse.fsbGetStatusLine()), NORMAL, " response (",
          INFO, fsBytesToHumanReadableString(len(oResponse.fsbSerialize())),
          [" ", fsCP437FromBytesString(oResponse.sb0MediaType)] if oResponse.sb0MediaType else [], NORMAL, ") received ",
          [INFO, "securely "] if oConnection.bSecure else [WARNING, "in plain text "], NORMAL,
          ["through proxy server at ", INFO, fsCP437FromBytesString(o0ProxyServerURL.sbAbsolute), NORMAL]
              if o0ProxyServerURL else
              ["from server at ", INFO, fsCP437FromBytesString(oConnection.foGetURLForRemoteServer().sbAbsolute), NORMAL],
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
      if bShowProgress:
        def fHandleHostnameResolved(oHTTPClient, sbHostname, iFamily, sCanonicalName, sIPAddress):
          sHostname = str(sbHostname, "ascii", "strict");
          if sHostname.lower() != sIPAddress.lower():
            oConsole.fOutput(
              "+ Hostname ", HILITE, sHostname, NORMAL, " resolved as ",
              INFO, sIPAddress, NORMAL, 
              [" (", INFO, sCanonicalName, NORMAL, ")"] if sCanonicalName.lower() != sHostname.lower() else [],
              "."
            );
          elif not sCanonicalName.startswith("%s:" % sIPAddress):
            oConsole.fOutput(
              "+ Hostname for IP address ", HILITE, sIPAddress, NORMAL, " is ",
              INFO, sCanonicalName, NORMAL,
              "."
            );
        oHTTPClient.fAddCallback("hostname resolved", fHandleHostnameResolved);
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
    
    # Helper function to get a single URL
    def foGetResponseForURL(oURL, uMaxRedirectsLeft, bFirstDownload):
      # Construct the HTTP request
      oRequest = oHTTPClient.foGetRequestForURL(
        oURL = oURL,
        sbzVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        s0Data = s0RequestData,
      );
      for (sbName, sbValue) in dsbAdditionalOrRemovedHeaders.items():
        if sbValue is None:
          oRequest.oHeaders.fbRemoveHeadersForName(sbName);
        else:
          oRequest.oHeaders.fbReplaceHeadersForName(sbName, sbValue);
      # Send the request and get the response.
      oConsole.fStatus(
        INFO, fsCP437FromBytesString(oRequest.sbVersion), " ", fsCP437FromBytesString(oRequest.sbMethod), " ", fsCP437FromBytesString(oURL.sbAbsolute), NORMAL, "...");
      try:
        o0Response = oHTTPClient.fo0GetResponseForRequestAndURL(oRequest, oURL);
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
        elif isinstance(oException, mExceptions.cHTTPFailedToConnectToProxyException):
          oConsole.fOutput(ERROR, "- Could not connect to proxy server:");
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
        oConsole.fOutput("  ", ERROR_INFO, str(oException.sMessage));
        for (sName, xValue) in oException.dxDetails.items():
          oConsole.fOutput("  ", ERROR, "\u2022 ", str(sName), " = ", ERROR_INFO, repr(xValue));
        sys.exit(4);
      if not o0Response:
        oConsole.fOutput(ERROR, "- No response received.");
        sys.exit(4);
      oResponse = o0Response;
      if uMaxRedirects and oResponse.uStatusCode in [301, 302, 307, 308]:
        oLocationHeader = oResponse.oHeaders.fo0GetUniqueHeaderForName(b"Location");
        if not oLocationHeader:
          oConsole.fOutput(ERROR, "- Redirected without a \"Location\" header.");
          sys.exit(4);
        sbRedirectToURL = oLocationHeader.sbValue;
        try:
          oURL = cURL.foFromBytesString(sbRedirectToURL);
        except mExceptions.cInvalidURLException as oException:
          oConsole.fOutput(ERROR, "Redirect to invalid URL ", ERROR_INFO, sbRedirectToURL, ERROR, ":");
          oConsole.fOutput("  ", ERROR_INFO, str(oException.sMessage));
          for (sName, xValue) in oException.dxDetails.items():
            oConsole.fOutput("  ", ERROR, "\u2022 ", str(sName), " = ", ERROR_INFO, repr(xValue));
          sys.exit(4);
        if bShowProgress:
          oConsole.fOutput(NORMAL, ">>> Redirected to URL: ", INFO, fsCP437FromBytesString(oURL.sbAbsolute), NORMAL, ".");
        if uMaxRedirectsLeft == 0:
          oConsole.fOutput(ERROR, "- Too many sequential redirects.");
          sys.exit(4);
        return foGetResponseForURL(oURL, uMaxRedirectsLeft - 1, bFirstDownload);
      if bDownload and oResponse.uStatusCode == 200:
        if s0DownloadToFilePath is None:
          sFilePath = oURL.asPath[-1];
          oDownloadToFile = cFileSystemItem(sFilePath);
        else:
          oDownloadToFile = cFileSystemItem(s0DownloadToFilePath);
          if not bFirstDownload:
            oDownloadToFile.fbOpenAsFile(bWritable = True, bAppend = True);
        sb0DecompressedBody = oResponse.sb0DecompressedBody or "";
        try:
          oDownloadToFile.fbWrite(sb0DecompressedBody, bThrowErrors = True);
        except Exception as oException:
          oConsole.fOutput(
            ERROR, "Cannot write ",
            ERROR_INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)),
            ERROR, "to file ",
            ERROR_INFO, oDownloadToFile.sPath,
            ERROR, ":"
          );
          oConsole.fOutput("  ", ERROR_INFO, str(oException.sMessage));
          for (sName, xValue) in oException.dxDetails.items():
            oConsole.fOutput("  ", ERROR, "\u2022 ", str(sName), " = ", ERROR_INFO, repr(xValue));
          sys.exit(6);
        if oDownloadToFile.fbIsOpenAsFile():
          oDownloadToFile.fbClose();
        if bShowProgress:
          oConsole.fOutput(
            "+ Saved ", INFO, fsBytesToHumanReadableString(len(sb0DecompressedBody)), NORMAL, " to ",
            INFO, oDownloadToFile.sPath, NORMAL, "."
          );
      return oResponse;
    
    if not bSegmentedVideo:
      oResponse = foGetResponseForURL(o0URL, uMaxRedirects, True);
    else:
      uIndex = uStartIndex;
      while 1:
        oURL = cURL.foFromBytesString(b"%s%d%s" % (sbURLSegmentHeader, uIndex, sbURLSegmentFooter));
        oResponse = foGetResponseForURL(oURL, uMaxRedirects, uIndex == uStartIndex);
        if oResponse.uStatusCode != 200:
          break;
        uIndex += 1;
      if bShowProgress:
        oConsole.fOutput("+ Found %d segments." % (uIndex - uStartIndex));
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException);
  raise;