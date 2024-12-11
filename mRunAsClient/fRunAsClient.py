import sys;

from mHTTPProtocol import (
  cHTTPInvalidMessageException,
  cHTTPRequest,
  cURL,
);
from mNotProvided import fbIsProvided;
  
from foConsoleLoader import foConsoleLoader;
from fOutputUsageInformation import fOutputUsageInformation;
from mColorsAndChars import (
    COLOR_ERROR, CHAR_ERROR,
    COLOR_INFO,
    COLOR_LIST, CHAR_LIST,
    COLOR_NORMAL,
);
from mExitCodes import (
  guExitCodeBadArgument,
  guExitCodeSuccess,
);
oConsole = foConsoleLoader();

from .fApplyHeaderSettingsToRequest import fApplyHeaderSettingsToRequest;
from .fProcessM3UFile import fProcessM3UFile;
from .fProcessSegmentedVideo import fProcessSegmentedVideo;
from .foGetHTTPClient import foGetHTTPClient;
from .foGetResponseForURL import foGetResponseForURL;
from .foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;

def fRunAsClient(
  *,
  bDecodeBodyOfHTTPMessages,
  bDownloadToFile,
  bFailOnDecodeBodyErrors,
  bForceHexOutputOfHTTPMessageBody,
  bProcessM3UFile,
  bProcessSegmentedM3U,
  bProcessSegmentedVideo,
  bSaveCookieStore,
  bSaveHTTPResponsesToFiles,
  bUseProxy,
  bVerifyCertificates,
  bShowDetails,
  bShowMessageBody,
  bShowProgress,
  bShowRequest,
  bShowResponse,
  d0SetForm_sValue_by_sName,
  d0SetJSON_sValue_by_sName,
  asbRemoveHeadersForLowerNames,
  dtsbReplaceHeaderNameAndValue_by_sLowerName,
  atsbAddHeadersNameAndValue,
  dsbSpoofedHost_by_sbHost,
  n0zTimeoutInSeconds,
  nSendDelayPerByteInSeconds,
  o0CookieStoreJSONFileSystemItem,
  o0DownloadToFileSystemItem,
  o0HTTPRequestFileSystemItem,
  o0HTTPProxyServerURL,
  o0SaveHTTPResponsesToFileSystemItem,
  o0URL,
  o0NetscapeCookiesFileSystemItem,
  s0SetHTTPRequestData,
  sb0SetHTTPRequestBody,
  sbzSetHTTPVersion,
  sbzSetMethod,
  u0MaxRedirects,
  uHexOutputCharsPerLine,
):
  if o0HTTPRequestFileSystemItem:
    oHTTPRequestFileSystemItem = o0HTTPRequestFileSystemItem;
    if bProcessSegmentedVideo:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Segmented videos using a HTTP request as input is not implemented.",
      );
      sys.exit(guExitCodeBadArgument);
    if bProcessM3UFile:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " M3U parsing using a HTTP request as input is not implemented.",
      );
      sys.exit(guExitCodeBadArgument);
    if d0SetForm_sValue_by_sName is not None:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Providing form values while using a HTTP request as input is not implemented.",
      );
      sys.exit(guExitCodeBadArgument);
    if d0SetJSON_sValue_by_sName is not None:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Providing JSON values while using a HTTP request as input is not implemented.",
      );
      sys.exit(guExitCodeBadArgument);
    if not oHTTPRequestFileSystemItem.fbIsFile():
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oHTTPRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " was not found.",
      );
      sys.exit(guExitCodeBadArgument);
    try:
      sbHTTPRequest = oHTTPRequestFileSystemItem.fsbRead();
    except:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oHTTPRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " could not be read.",
      );
      sys.exit(guExitCodeBadArgument);
    try:
      oHTTPRequest = cHTTPRequest.foFromBytesString(sbHTTPRequest);
    except cHTTPInvalidMessageException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oHTTPRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " could not be parsed.",
      );
      oConsole.fOutput(
        COLOR_NORMAL, "  ",
        COLOR_INFO, oException.sMessage,
      );
      for (sName, xValue) in oException.dxDetails:
        oConsole.fOutput(
          COLOR_NORMAL, "  ",
          COLOR_LIST, CHAR_LIST,
          COLOR_NORMAL, " ",
          COLOR_INFO, sName,
          COLOR_NORMAL, " = ",
          COLOR_INFO, str(xValue),
        );
      sys.exit(guExitCodeBadArgument);
    if fbIsProvided(sbzSetHTTPVersion):
      oHTTPRequest.sbHTTPVersion = sbzSetHTTPVersion;
    if fbIsProvided(sbzSetMethod):
      oHTTPRequest.sbMethod = sbzSetMethod;
    # When setting the body, we automatically set the `Content-Length` header.
    # This can be removed or modified using the header arguments immediately after
    if sb0SetHTTPRequestBody is not None:
      oHTTPRequest.fSetBody(sb0SetHTTPRequestBody, bAddContentLengthHeader = True);
    if s0SetHTTPRequestData is not None:
      oHTTPRequest.fSetData(s0SetHTTPRequestData, bAddContentLengthHeader = True);
    # Apply header arguments:
    fApplyHeaderSettingsToRequest(asbRemoveHeadersForLowerNames, dtsbReplaceHeaderNameAndValue_by_sLowerName, atsbAddHeadersNameAndValue);
    if o0URL is None:
      s0Extension = oHTTPRequestFileSystemItem.s0Extension.lower() if oHTTPRequestFileSystemItem.s0Extension else None;
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
  
  if d0SetForm_sValue_by_sName and d0SetJSON_sValue_by_sName is not None:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Providing form and JSON values simultaneously is not implemented.",
    );
    sys.exit(guExitCodeBadArgument);
  ### HTTP CLIENT #############################################################
  oHTTPClient = foGetHTTPClient(
    bUseProxy = bUseProxy,
    o0HTTPProxyServerURL = o0HTTPProxyServerURL,
    n0zTimeoutInSeconds = n0zTimeoutInSeconds,
    nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
    bVerifyCertificates = bVerifyCertificates,
    bShowMessageBody = bShowMessageBody,
    bShowProgress = bShowProgress,
    bShowRequest = bShowRequest,
    bShowResponse = bShowResponse,
    bShowDetails = bShowDetails,
    bDecodeBodyOfHTTPMessages = bDecodeBodyOfHTTPMessages,
    bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
    bForceHexOutputOfHTTPMessageBody = bForceHexOutputOfHTTPMessageBody,
    uHexOutputCharsPerLine = uHexOutputCharsPerLine,
    o0NetscapeCookiesFileSystemItem = o0NetscapeCookiesFileSystemItem,
    bSaveCookieStore = bSaveCookieStore,
    o0CookieStoreJSONFileSystemItem = o0CookieStoreJSONFileSystemItem,
    dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
  );
  try:
    if oHTTPClient.o0CookieStore and o0HTTPRequest:
      oHTTPClient.o0CookieStore.fApplyToRequestForURL(o0HTTPRequest, oURL);
    
    if bProcessM3UFile:
      assert not o0HTTPRequest; # This should have been prevented when parsing the arguments.
      ### M3U ######################################################################
      fProcessM3UFile(
        oHTTPClient = oHTTPClient,
        oURL = oURL,
        sbzSetHTTPVersion = sbzSetHTTPVersion,
        sbzSetMethod = sbzSetMethod,
        sb0SetHTTPRequestBody = sb0SetHTTPRequestBody,
        s0SetHTTPRequestData = s0SetHTTPRequestData,
        asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
        dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
        atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
        d0SetForm_sValue_by_sName = d0SetForm_sValue_by_sName,
        d0SetJSON_sValue_by_sName = d0SetJSON_sValue_by_sName,
        u0MaxRedirects = u0MaxRedirects,
        bDownloadToFile = bDownloadToFile,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
        o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
        o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
        bShowProgress = bShowProgress,
        bProcessSegmentedM3U = bProcessSegmentedM3U,
      );
    elif bProcessSegmentedVideo:
      assert not o0HTTPRequest; # This should have been prevented when parsing the arguments.
      ### SEGMENTED VIDEO ##########################################################
      # Multiple request to URL with increasing index until we get a response that is not "200 Ok"
      fProcessSegmentedVideo(
        oHTTPClient = oHTTPClient,
        oURL = oURL,
        sbzSetHTTPVersion = sbzSetHTTPVersion,
        sbzSetMethod = sbzSetMethod,
        sb0SetHTTPRequestBody = sb0SetHTTPRequestBody,
        s0SetHTTPRequestData = s0SetHTTPRequestData,
        asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
        dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
        atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
        d0SetForm_sValue_by_sName = d0SetForm_sValue_by_sName,
        d0SetJSON_sValue_by_sName = d0SetJSON_sValue_by_sName,
        u0MaxRedirects = u0MaxRedirects,
        bDownloadToFile = bDownloadToFile,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
        o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
        o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
        bShowProgress = bShowProgress,
      );
    elif o0HTTPRequest is None:
      ### URL ######################################################################
      # Single request from URL
      foGetResponseForURL(
        oHTTPClient = oHTTPClient,
        oURL = oURL,
        sbzSetHTTPVersion = sbzSetHTTPVersion,
        sbzSetMethod = sbzSetMethod,
        sb0SetHTTPRequestBody = sb0SetHTTPRequestBody,
        s0SetHTTPRequestData = s0SetHTTPRequestData,
        asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
        dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
        atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
        d0SetForm_sValue_by_sName = d0SetForm_sValue_by_sName,
        d0SetJSON_sValue_by_sName = d0SetJSON_sValue_by_sName,
        u0MaxRedirects = u0MaxRedirects,
        bDownloadToFile = bDownloadToFile,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
        o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
        o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
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
        bSaveHTTPResponsesToFiles = bSaveHTTPResponsesToFiles,
        o0DownloadToFileSystemItem = o0DownloadToFileSystemItem,
        o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
        bConcatenateDownload = False,
        bShowProgress = bShowProgress,
      );
  finally:
    oHTTPClient.fStop();