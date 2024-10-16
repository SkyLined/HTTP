"""                                                    _   _                  
           ┄┄┄┄┄┄┄┄╒╦╦┄┄╦╦╕┄╒═╦╦═╕┄╒═╦╦═╕┄╒╦╦══╦╗┄┄▄┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄          
                    ║╠══╣║    ║║     ║║    ║╠══╩╝    ╱╱  ╱╱                   
         ┄┄┄┄┄┄┄┄┄┄╘╩╩┄┄╩╩╛┄┄╘╩╩╛┄┄┄╘╩╩╛┄┄╘╩╩╛┄┄┄┄▀┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄            
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
  from mFileSystemItem import cFileSystemItem;
  from mHTTPClient import cURL;
  from mHTTPProtocol import cHTTPRequest;
  from mNotProvided import fbIsProvided, zNotProvided;
  
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from foConsoleLoader import foConsoleLoader;
  from fOutputExceptionAndExit import fOutputExceptionAndExit;
  from fOutputUsageInformation import fOutputUsageInformation;
  from mColorsAndChars import (
    COLOR_ERROR, CHAR_ERROR,
    COLOR_INFO, 
    COLOR_NORMAL
  );
  from mExitCodes import (
    guExitCodeBadArgument,
    guExitCodeCannotReadRequestBodyFromFile,
    guExitCodeRequestDataInFileIsNotUTF8,
    guExitCodeSuccess,
  );
  from mRunAsClient import (
    fHandleM3U,
    fHandleSegmentedVideo,
    foGetHTTPClient,
    foGetResponseForURL,
    foGetResponseForRequestAndURL,
  );
  oConsole = foConsoleLoader();

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


  if __name__ == "__main__":
    rShouldBeAURL = re.compile(r"^https?://.*$", re.I);
    rMethod = re.compile(r"^[A-Z]+$", re.I);
    rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
    rCharEncoding = re.compile(r"([^\\]+)|\\(?:x([0-9a-f]{2}))?", re.I);
    
    asArguments = sys.argv[1:];
    dsbAdditionalOrRemovedHeaders = {};
    d0Form_sValue_by_sName = None;
    sbzHTTPVersion = zNotProvided;
    sbzMethod = zNotProvided;
    o0URL = None;
    o0HTTPFile = None;
    bM3U = False;
    bSegmentedM3U = False;
    bSegmentedVideo = None;
    uStartIndex = None;
    bzShowProgress = zNotProvided;
    bzShowRequest = zNotProvided;
    bzShowResponse = zNotProvided;
    bzShowDetails = zNotProvided;
    bShowProxyConnects = False;
    bUseProxy = False;
    o0HTTPProxyServerURL = None;
    sb0RequestBody = None;
    s0RequestData = None;
    bDecodeBody = False;
    bFailOnDecodeBodyErrors = False;
    u0MaxRedirects = None;
    bVerifyCertificates = True;
    bSaveToFile = False;
    bDownloadToFile = False;
    s0TargetFilePath = None;
    s0zCookieStoreJSONPath = zNotProvided;
    s0NetscapeCookiesFilePath = None;
    n0zTimeoutInSeconds = zNotProvided;
    dsbSpoofedHost_by_sbHost = {};
    bForceHex = False;
    uHexChars = 16;
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
      if not s0LowerName:
        if o0URL is None and rShouldBeAURL.match(sArgument):
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
          o0HTTPFile = cFileSystemItem(sArgument);
          if not o0HTTPFile.fbIsFile():
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Superfluous argument \"",
              COLOR_INFO, sArgument,
              COLOR_NORMAL, "\".",
            );
            oConsole.fOutput(
              COLOR_NORMAL, "  It is neither a HTTP method, version, URL or an existing input file.",
            );
            sys.exit(guExitCodeBadArgument);
      elif s0LowerName in ["bl", "basic-login"]:
        sbBase64EncodedUserNameColonPassword = base64.b64encode(bytes(ord(s) for s in (s0Value or "")));
        dsbAdditionalOrRemovedHeaders[b"Authorization"] = b"basic %s" % sbBase64EncodedUserNameColonPassword;
      elif s0LowerName in ["c", "cookies"]:
        s0NetscapeCookiesFilePath = s0Value;
      elif s0LowerName in ["s", "cs", "cookie-store"]:
        s0zCookieStoreJSONPath = s0Value;
      elif s0LowerName in ["data"]:
        sb0RequestBody = None;
        s0RequestData = fsRequireArgumentValue();
      elif s0LowerName in ["bf", "body-file"]:
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
          sb0RequestBody = oDataFileSystemItem.fsbRead();
          s0RequestData = None;
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot read from file ",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, ".",
          );
          fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
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
          sbFileContent = oDataFileSystemItem.fsbRead();
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot read from file ",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, ".",
          );
          fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
        try:
          sb0RequestBody = None;
          s0RequestData = str(sbFileContent, "utf-8", "strict");
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " File ",
            COLOR_INFO, oDataFileSystemItem.sPath,
            COLOR_NORMAL, " does not contain utf-8 encoded data.",
          );
          fOutputExceptionAndExit(oException, guExitCodeRequestDataInFileIsNotUTF8);
      elif s0LowerName in ["debug"]:
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
      elif s0LowerName in ["db", "decode", "decode-body"]:
        bDecodeBody = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["fail-on-decode-errors", "report-decode-body-errors"]:
        bFailOnDecodeBodyErrors = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["dl", "download"]:
        bDownloadToFile = True;
        s0TargetFilePath = s0Value;
      elif s0LowerName in ["form"]:
        sValue = fsRequireArgumentValue();
        tsFormNameAndValue = sValue.split("=", 1);
        if len(tsFormNameAndValue) == 1:
          sName = sValue; sValue = "";
        else:
          sName, sValue = tsFormNameAndValue;
        if d0Form_sValue_by_sName is None:
          d0Form_sValue_by_sName = {};
        d0Form_sValue_by_sName[sName] = sValue;
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
      elif s0LowerName in ["hex"]:
        bForceHex = True;
        # If a path is provided for downloading, set it.
        if s0Value is not None:
          try:
            uHexChars = int(s0Value);
            assert uHexChars > 0;
          except (ValueError, AssertionError):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " The value for \"",
              COLOR_INFO, sArgument,
              COLOR_NORMAL, "\" must be a positive integer number greater than zero.",
            );
            sys.exit(guExitCodeBadArgument);
      elif s0LowerName in ["m3u"]:
        bM3U = True;
        bDownloadToFile = True;
        # If a path is provided for downloading, set it.
        if s0Value is not None:
          s0TargetFilePath = s0Value;
      elif s0LowerName in ["sm3u", "segmented-m3u"]:
        bM3U = True;
        bDownloadToFile = True;
        bSegmentedM3U = True;
        if s0Value is not None:
          s0TargetFilePath = s0Value;
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
      elif s0LowerName in ["r", "max-redirects", "follow-redirects"]:
        if s0Value:
          try:
            u0MaxRedirects = int(s0Value);
            assert u0MaxRedirects >= 0, "";
          except:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " The value for \"",
              COLOR_INFO, sArgument,
              COLOR_NORMAL, "\" must be a positive integer number or zero.",
            );
            sys.exit(guExitCodeBadArgument);
        else:
          u0MaxRedirects = 32;
      elif s0LowerName in ["save"]:
        bSaveToFile = True;
        s0TargetFilePath = s0Value;
      elif s0LowerName in ["secure"]:
        bVerifyCertificates = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["insecure", "non-secure"]:
        bVerifyCertificates = not fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["sv", "segmented-video"]:
        bSegmentedVideo = True;
        bDownloadToFile = True;
        # If a path is provided for downloading, set it. If not, make sure we download by setting it to None
        if s0Value:
          s0TargetFilePath = s0Value;
      elif s0LowerName in ["show-details"]:
        bzShowDetails = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-progress"]:
        bzShowProgress = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-request"]:
        bzShowRequest = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["show-response"]:
        bzShowResponse = fbParseBooleanArgument(s0Value);
      elif s0LowerName in ["t", "timeout"]:
        if s0Value is None or s0Value.lower() == "none":
          n0zTimeoutInSeconds = None;
        else:
          try:
            n0zTimeoutInSeconds = float(s0Value);
            assert n0zTimeoutInSeconds > 0, "";
          except:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " The value for \"",
              COLOR_INFO, sArgument,
              COLOR_NORMAL, "\" must be a number larger than zero.",
            );
            sys.exit(guExitCodeBadArgument);
      elif s0LowerName.startswith("spoof:"):
        sbHost = bytes(ord(s) for s in s0LowerName.split(":", 1)[1]);
        sbIPaddress = bytes(ord(s) for s in fsRequireArgumentValue());
        dsbSpoofedHost_by_sbHost[sbHost] = sbIPaddress;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Unknown argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);

    ### DONE PARSING ARGUMENTS #################################################
    if o0HTTPFile:
      oHTTPFile = o0HTTPFile;
      sbHTTPRequest = oHTTPFile.fsbRead();
      oHTTPRequest = cHTTPRequest.foFromBytesString(sbHTTPRequest);
      if bSegmentedVideo:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Segmented videos using a HTTP request as input is not implemented.",
        );
        sys.exit(guExitCodeBadArgument);
      if bM3U:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " M2U parsing using a HTTP request as input is not implemented.",
        );
        sys.exit(guExitCodeBadArgument);
      if d0Form_sValue_by_sName is not None:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Providing form values while using a HTTP request as input is not implemented.",
        );
        sys.exit(guExitCodeBadArgument);
      if fbIsProvided(sbzHTTPVersion):
        oHTTPRequest.sbHTTPVersion = sbzHTTPVersion;
      if fbIsProvided(sbzMethod):
        oHTTPRequest.sbMethod = sbzMethod;
      if sb0RequestBody is not None:
        oHTTPRequest.fSetBody(sb0RequestBody);
      if s0RequestData is not None:
        oHTTPRequest.fSetData(s0RequestData);
      for (sbName, sbValue) in dsbAdditionalOrRemovedHeaders.items():
        if sbValue is None:
          oHTTPRequest.oHeaders.fbRemoveHeadersForName(sbName);
        else:
          oHTTPRequest.oHeaders.fbReplaceHeadersForNameAndValue(sbName, sbValue);
      if o0URL is None:
        s0Extension = oHTTPFile.s0Extension.lower() if oHTTPFile.s0Extension else None;
        if s0Extension not in ["http", "https"]:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot determine the protocol to use because the HTTP request input file does",
          );
          oConsole.fOutput(
            "  not have a .http(s) extension and no URL was provided.",
          );
          sys.exit(guExitCodeBadArgument);
        sbProtocol = bytes(ord(s) for s in s0Extension);
        o0HostHeader = oHTTPRequest.oHeaders.fo0GetUniqueHeaderForName(b"Host");
        if o0HostHeader is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot determine the server to connect to because the HTTP request input file",
          );
          oConsole.fOutput(
            "  does not contain a 'Host' header and no URL was provided.",
          );
          sys.exit(guExitCodeBadArgument);
        sbURL = b"%s://%s%s" % (
          sbProtocol,
          o0HostHeader.sbValue,
          oHTTPRequest.sbURL,
        );
        oURL = cURL.foFromBytesString(sbURL);
      else:
        oURL = o0URL;
      o0HTTPRequest = oHTTPRequest;
    elif o0URL:
      oURL = o0URL;
      o0HTTPRequest = None;
    else:
      fOutputUsageInformation(bOutputAllOptions = False);
      sys.exit(guExitCodeSuccess);
    
    # If not explicitly set, show progress
    bShowProgress = bzShowProgress if fbIsProvided(bzShowProgress) else True;
    # If not explicitly set, only show requests and responses when we are not downloading.
    bShowRequestResponseDefault = not (bDownloadToFile or bSaveToFile);
    bShowRequest = bzShowRequest if fbIsProvided(bzShowRequest) else bShowRequestResponseDefault;
    bShowResponse = bzShowResponse if fbIsProvided(bzShowResponse) else bShowRequestResponseDefault;
    bShowDetails = bzShowDetails if fbIsProvided(bzShowDetails) else False;
    
    ### HTTP CLIENT #############################################################
    bSaveCookiesToDisk = fbIsProvided(s0zCookieStoreJSONPath);
    oHTTPClient = foGetHTTPClient(
      bUseProxy = bUseProxy,
      o0HTTPProxyServerURL = o0HTTPProxyServerURL,
      n0zTimeoutInSeconds = n0zTimeoutInSeconds,
      bVerifyCertificates = bVerifyCertificates,
      bShowProgress = bShowProgress,
      bShowProxyConnects = bShowProxyConnects,
      bShowRequest = bShowRequest,
      bShowResponse = bShowResponse,
      bShowDetails = bShowDetails,
      bDecodeBody = bDecodeBody,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bForceHex = bForceHex,
      uHexChars = uHexChars,
      s0NetscapeCookiesFilePath = s0NetscapeCookiesFilePath,
      bSaveCookiesToDisk = bSaveCookiesToDisk,
      s0zCookieStoreJSONPath = s0zCookieStoreJSONPath,
      dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
    );
    try:
      if oHTTPClient.o0CookieStore and o0HTTPRequest:
        oHTTPClient.o0CookieStore.fApplyToRequestForURL(o0HTTPRequest, oURL);
      
      if bM3U:
        ### M3U ######################################################################
        fHandleM3U(
          oHTTPClient = oHTTPClient,
          oURL = oURL,
          sbzHTTPVersion = sbzHTTPVersion,
          sbzMethod = sbzMethod,
          sb0RequestBody = sb0RequestBody,
          s0RequestData = s0RequestData,
          dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName = d0Form_sValue_by_sName,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bShowProgress = bShowProgress,
          bSegmentedM3U = bSegmentedM3U,
        );
      elif bSegmentedVideo:
        ### SEGMENTED VIDEO ##########################################################
        # Multiple request to URL with increasing index until we get a response that is not "200 Ok"
        fHandleSegmentedVideo(
          oHTTPClient = oHTTPClient,
          oURL = oURL,
          sbzHTTPVersion = sbzHTTPVersion,
          sbzMethod = sbzMethod,
          sb0RequestBody = sb0RequestBody,
          s0RequestData = s0RequestData,
          dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName = d0Form_sValue_by_sName,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bShowProgress = bShowProgress,
        );
      elif o0HTTPRequest is None:
        ### URL ######################################################################
        # Single request from URL
        foGetResponseForURL(
          oHTTPClient = oHTTPClient,
          oURL = oURL,
          sbzHTTPVersion = sbzHTTPVersion,
          sbzMethod = sbzMethod,
          sb0RequestBody = sb0RequestBody,
          s0RequestData = s0RequestData,
          dsbAdditionalOrRemovedHeaders = dsbAdditionalOrRemovedHeaders,
          d0Form_sValue_by_sName = d0Form_sValue_by_sName,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bConcatenateDownload = False,
          bShowProgress = bShowProgress,
        );
      else:
        ### .HTTP(S) FILE ############################################################
        # Single request
        foGetResponseForRequestAndURL(
          oHTTPClient = oHTTPClient,
          oRequest = o0HTTPRequest,
          oURL = oURL,
          u0MaxRedirects = u0MaxRedirects,
          bDownloadToFile = bDownloadToFile,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bSaveToFile = bSaveToFile,
          s0TargetFilePath = s0TargetFilePath,
          bConcatenateDownload = False,
          bShowProgress = bShowProgress,
        );
    finally:
      oHTTPClient.fStop();
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;