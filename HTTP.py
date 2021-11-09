"""                                                      _   _                  
           ┄┄┄┄┄┄┄┄╒╦╦┄┄╦╦╕┄╒═╦╦═╕┄╒═╦╦═╕┄╒╦╦══╦╗┄┄┄┄┄┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄          
                    ║╠══╣║    ║║     ║║    ║╠══╩╝  □   ╱╱  ╱╱                   
         ┄┄┄┄┄┄┄┄┄┄╘╩╩┄┄╩╩╛┄┄╘╩╩╛┄┄┄╘╩╩╛┄┄╘╩╩╛┄┄┄┄┄□┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄            
                                                      ‾   ‾                  """;
import base64, os, re, sys;

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

guExitCodeInternalError = 1; # Just in case mExitCodes is not loaded, as we need this later.
try:
  from mConsole import oConsole;
  from mFileSystemItem import cFileSystemItem;
  from mHTTPClient import cHTTPClient, cHTTPClientUsingProxyServer, cHTTPClientUsingAutomaticProxyServer, cHTTPHeaders, cURL, mExceptions;
  from mNotProvided import *;
  
  from cSession import cSession;
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from fbApplySessionJSONToSession import fbApplySessionJSONToSession;
  from foGetResponseForURL import foGetResponseForURL;
  from fOutputExceptionAndExit import fOutputExceptionAndExit;
  from fOutputHostnameResolved import fOutputHostnameResolved;
  from fOutputRequestSent import fOutputRequestSent;
  from fOutputResponseReceived import fOutputResponseReceived;
  from fOutputSessionExpiredCookie import fOutputSessionExpiredCookie;
  from fOutputSessionInvalidCookieAttributeAndExit import fOutputSessionInvalidCookieAttributeAndExit;
  from fOutputSessionSetCookie import fOutputSessionSetCookie;
  from mCP437 import fsCP437FromBytesString;
  from mColorsAndChars import *;
  from mExitCodes import *;
  
  if __name__ == "__main__":
    rURL = re.compile(r"^https?://.*$", re.I);
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
    sbzMethod = zNotProvided;
    o0URL = None;
    bSegmentedVideo = None;
    uStartIndex = None;
    oSession = cSession();
    bShowProgress = True;
    bShowRequest = True;
    bShowResponse = True;
    bShowDetails = True;
    bUseProxy = False;
    o0HTTPProxyServerURL = None;
    s0RequestData = None;
    bDecodeBody = False;
    u0MaxRedirects = None;
    bAllowUnverifiableCertificates = False;
    s0zDownloadToFilePath = zNotProvided;
    s0zSessionPath = zNotProvided;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      def fbParseBooleanArgument():
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
        if fbParseBooleanArgument():
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
        if not oDataFileSystemItem.fbIsFile(bParseZipFiles = True):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot find file \"",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, "\"."
          );
          sys.exit(guExitCodeBadArgument);
        try:
          sbRequestData = oDataFileSystemItem.fsbRead(bParseZipFiles = True, bThrowErrors = true);
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
        bDecodeBody = fbParseBooleanArgument();
      elif s0LowerName in ["dl", "download"]:
        s0zDownloadToFilePath = s0Value;
      elif s0LowerName in ["s", "session"]:
        s0zSessionPath = s0Value;
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
      elif s0LowerName in ["sv", "segmented-video"]:
        bSegmentedVideo = True;
        # If a path is provided for downloading, set it. If not, make sure we download by setting it to None
        if s0Value is not None or not fbIsProvided(s0zDownloadToFilePath):
          s0zDownloadToFilePath = s0Value;
      elif s0LowerName in ["s", "secure"]:
        bAllowUnverifiableCertificates = fbParseBooleanArgument();
      elif s0LowerName in ["show-progress"]:
        bShowProgress = fbParseBooleanArgument();
      elif s0LowerName in ["show-request"]:
        bShowRequest = fbParseBooleanArgument();
      elif s0LowerName in ["show-response"]:
        bShowResponse = fbParseBooleanArgument();
      elif s0LowerName in ["show-details"]:
        bShowDetails = fbParseBooleanArgument();
      elif s0LowerName:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Unknown argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      elif o0URL is None and rURL.match(sArgument):
        o0URL = cURL.foFromBytesString(bytes(ord(s) for s in sArgument));
      elif not fbIsProvided(sbzMethod) and rMethod.match(sArgument):
        sbzMethod = bytes(ord(s) for s in sArgument);
      elif not fbIsProvided(oSession.sbzHTTPVersion) and rHTTPVersion.match(sArgument):
        oSession.sbzHTTPVersion = bytes(ord(s) for s in sArgument);
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
    if bSegmentedVideo:
      for rbSegmentedVideo in arbSegmentedVideos:
        obURLSegmentMatch = rbSegmentedVideo.match(o0URL.sbAbsolute);
        if obURLSegmentMatch:
          break;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not identify segmentation from URL \"",
          COLOR_INFO, sURL,
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
    ### HTTP CLIENT ###########################################################
    # We need to use a HTTP client with no proxy, a static proxy or a dynamic
    # proxy. We'll create an instance of the right type of HTTP client now and
    # add event handlers for reporting requests and responses to the user.
    
    # Since the event arguments differ for each type of HTTP client, event
    # handlers specific to the client are created which call into the following
    # two generic functions for reporting the requests/reponses:
    if not bUseProxy:
      # Create a HTTP client instance that uses no proxy
      oHTTPClient = cHTTPClient(bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
      # Create event handlers specific to this situation that call the generic request/response reporters
      def fRequestSentEventHandler(oHTTPClient, oConnection, oRequest):
        fOutputRequestSent(
          oConnection, oRequest, None, # 3rd argument == None => Did not use a proxy
          bShowProgress, bShowRequest, bShowDetails, bDecodeBody,
        );
      def fResponseReceivedEventHandler(oHTTPClient, oConnection, oResponse):
        fOutputResponseReceived(
          oConnection, oResponse, None, # 3rd argument == None => Did not use a proxy
          bShowProgress, bShowResponse, bShowDetails, bDecodeBody,
        );
      if bShowProgress:
        def fHostnameResolvedEventHandler(oHTTPClient, sbHostname, iFamily, sCanonicalName, sIPAddress):
          fOutputHostnameResolved(sbHostname, sCanonicalName, sIPAddress);
        oHTTPClient.fAddCallback("hostname resolved", fHostnameResolvedEventHandler);
    elif o0HTTPProxyServerURL:
      # Create a HTTP client instance that uses a static proxy
      oHTTPClient = cHTTPClientUsingProxyServer(o0HTTPProxyServerURL, bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
      # Create event handlers specific to this situation that call the generic request/response reporters
      def fRequestSentEventHandler(oHTTPClient, oConnection, oRequest):
        fOutputRequestSent(
          oConnection, oRequest, oHTTPClient.oProxyServerURL, # 3rd argument == URL => Used a proxy
          bShowProgress, bShowRequest, bShowDetails, bDecodeBody,
        );
      def fResponseReceivedEventHandler(oHTTPClient, oConnection, oResponse):
        fOutputResponseReceived(
         oConnection, oResponse, oHTTPClient.oProxyServerURL,# 3rd argument == URL => Used a proxy
         bShowProgress, bShowResponse, bShowDetails, bDecodeBody,
       ); 
    else:
      # Create a HTTP client instance that uses dynamic proxies.
      oHTTPClient = cHTTPClientUsingAutomaticProxyServer(bAllowUnverifiableCertificates = bAllowUnverifiableCertificates);
      def fRequestSentEventHandler(oHTTPClient, oSecondaryHTTPClient, o0ProxyServerURL, oConnection, oRequest):
        fOutputRequestSent(
          oConnection, oRequest, o0ProxyServerURL, # 3rd argument == None/URL => May have used a proxy
          bShowProgress, bShowRequest, bShowDetails, bDecodeBody,
        );
      def fResponseReceivedEventHandler(oHTTPClient, oSecondaryHTTPClient, o0ProxyServerURL, oConnection, oResponse):
        fOutputResponseReceived(
          oConnection, oResponse, o0ProxyServerURL, # 3rd argument == None/URL => May have used a proxy
          bShowProgress, bShowResponse, bShowDetails, bDecodeBody,
        );
    # If needed, apply the event handlers specific to this situation which where created above:
    if bShowProgress or bShowRequest:
      oHTTPClient.fAddCallback("request sent", fRequestSentEventHandler);
    if bShowProgress or bShowResponse:
      oHTTPClient.fAddCallback("response received", fResponseReceivedEventHandler);
    
    ### SESSION FILE ##########################################################
    if fbIsProvided(s0zSessionPath) and s0zSessionPath is not None:
      oSessionFileOrFolder = cFileSystemItem(s0zSessionPath);
      if oSessionFileOrFolder.fbIsFolder():
        o0SessionFile = oSessionFileOrFolder.foGetChild("http-session.json");
      elif oSessionFileOrFolder.fbIsFile():
        o0SessionFile = oSessionFileOrFolder;
      elif oSessionFileOrFolder.oParent.fbIsFolder():
        o0SessionFile = oSessionFileOrFolder;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not find session file ",
          COLOR_INFO, oSessionFileOrFolder.sPath,
          COLOR_NORMAL, ".",
        );
        sys.exit(guExitCodeBadArgument);
    else:
      o0SessionFile = None;
    
    if o0SessionFile and o0SessionFile.fbIsFile():
      if bShowProgress:
        oConsole.fOutput(
          COLOR_INFO, CHAR_INFO,
          COLOR_NORMAL, " Session settings:",
        );
        oConsole.fStatus(
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Loading session from file ",
          COLOR_INFO, o0SessionFile.sPath,
          COLOR_NORMAL, "...",
        );
      try:
        sbSessionFileJSON = o0SessionFile.fsbRead(bThrowErrors = True);
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not read session file ",
          COLOR_INFO, o0SessionFile.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadSessionFromFile);
      if bShowProgress:
        oConsole.fStatus(
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Parsing session file ",
          COLOR_INFO, o0SessionFile.sPath,
          COLOR_NORMAL, "...",
        );
      def fOutputSessionHTTPVersion(oSession, sbHTTPVersion):
        oConsole.fOutput(
          "  ",
          CHAR_LIST,
          COLOR_NORMAL, " HTTP version: ",
          COLOR_INFO, fsCP437FromBytesString(sbHTTPVersion),
          COLOR_NORMAL, ".",
        );
      def fOutputSessionMaxRedirects(oSession, u0MaxRedirects):
        if u0MaxRedirects is None:
          oConsole.fOutput(
            "  ",
            CHAR_LIST,
            COLOR_NORMAL, " Redirects: ",
            COLOR_INFO, "not followed",
            COLOR_NORMAL, ".",
          );
        else:
          oConsole.fOutput(
            "  ",
            CHAR_LIST,
            COLOR_NORMAL, " Max redirects: ",
            COLOR_INFO, str(u0MaxRedirects),
            COLOR_NORMAL, ".",
          );
      def fOutputSessionUserAgent(oSession, sbUserAgent):
        oConsole.fOutput(
          "  ",
          CHAR_LIST,
          COLOR_NORMAL, " User agent: ",
          COLOR_INFO, fsCP437FromBytesString(sbUserAgent),
          COLOR_NORMAL, ".",
        );
      def fOutputSessionDoNotTrackHeader(oSession, bDoNotTrack):
        oConsole.fOutput(
          "  ",
          CHAR_LIST,
          COLOR_NORMAL, " Do not track: ",
          COLOR_INFO,
          "" if bDoNotTrack else "do NOT ", "add \"DNT: 1\" header",
          COLOR_NORMAL, ".",
        );
      def fApplySessionJSONAddCookieEventHandler(oSession, sbOrigin, oCookie):
        fOutputSessionSetCookie(sbOrigin, oCookie, False, False); # 3rd argument: cookie is added, 4rth argument, cookie is modified.
      try:
        bSessionJSONHasData = fbApplySessionJSONToSession(
          sbSessionFileJSON,
          oSession,
          f0SetHTTPVersionCallback = fOutputSessionHTTPVersion if bShowProgress else None,
          f0SetMaxRedirectsCallback = fOutputSessionMaxRedirects if bShowProgress else None,
          f0SetUserAgentCallback = fOutputSessionUserAgent if bShowProgress else None,
          f0SetAddDoNotTrackHeaderCallback = fOutputSessionDoNotTrackHeader if bShowProgress else None,
          f0AddCookieCallback = fApplySessionJSONAddCookieEventHandler if bShowProgress else None,
        );
      except ValueError as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Could not parse session file ",
          COLOR_INFO, o0SessionFile.sPath,
          COLOR_NORMAL, ":",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadSessionFromFile);
      if bShowProgress and not bSessionJSONHasData:
        oConsole.fOutput(
          "  (Session file has not data).",
        );
    if not bSegmentedVideo:
      # Single request
      foGetResponseForURL(
        oHTTPClient,
        o0SessionFile, oSession,
        o0URL, sbzMethod, s0RequestData,
        dsbAdditionalOrRemovedHeaders,
        d0Form_sValue_by_sName,
        u0MaxRedirects,
        s0zDownloadToFilePath, True, # bIsFirstDownload
        bShowProgress,
      );
    else:
      # Multiple request to URL with increasing index until we get a response that is not "200 COLOR_OK"
      uIndex = uStartIndex;
      while 1:
        oURL = cURL.foFromBytesString(b"%s%d%s" % (sbURLSegmentHeader, uIndex, sbURLSegmentFooter));
        oResponse = foGetResponseForURL(
          oHTTPClient,
          o0SessionFile, oSession,
          oURL, sbzMethod, s0RequestData,
          dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName,
          u0MaxRedirects,
          s0zDownloadToFilePath, uIndex == uStartIndex, # bIsFirstDownload
          bShowProgress,
        );
        if oResponse.uStatusCode != 200:
          break;
        uIndex += 1;
      if bShowProgress:
        oConsole.fOutput(
          COLOR_OK, CHAR_OK,
          COLOR_NORMAL, "+ Found ",
          COLOR_INFO, str(uIndex - uStartIndex),
          COLOR_NORMAL, " segments.",
        );
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;