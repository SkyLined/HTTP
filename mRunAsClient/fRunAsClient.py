import sys;

from mHTTPProtocol import (
  cRequest,
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

from .fApplyBodyToRequest import fApplyBodyToRequest;
from .fApplyHeaderSettingsToRequest import fApplyHeaderSettingsToRequest;
from .fProcessM3UFile import fProcessM3UFile;
from .fProcessSegmentedVideo import fProcessSegmentedVideo;
from .foGetClient import foGetClient;
from .foGetResponseForURL import foGetResponseForURL;
from .foGetResponseForRequestAndURL import foGetResponseForRequestAndURL;

def fRunAsClient(
  *,
  bAddContentLengthHeaderForBody,
  bApplyChunkedEncodingToBody,
  bCompressBody,
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
  o0RequestFileSystemItem,
  o0ProxyServerURL,
  o0SaveHTTPResponsesToFileSystemItem,
  o0URL,
  o0NetscapeCookiesFileSystemItem,
  sx0Body,
  sbzHTTPVersion,
  sbzMethod,
  u0MaxRedirects,
  uHexOutputCharsPerLine,
):
  if o0RequestFileSystemItem:
    oRequestFileSystemItem = o0RequestFileSystemItem;
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
    if not oRequestFileSystemItem.fbIsFile():
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " was not found.",
      );
      sys.exit(guExitCodeBadArgument);
    try:
      sbHTTPRequest = oRequestFileSystemItem.fsbRead();
    except:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " could not be read.",
      );
      sys.exit(guExitCodeBadArgument);
    try:
      oRequest = cRequest.foFromBytesString(sbHTTPRequest);
    except cInvalidMessageException as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The HTTP request input file ",
        COLOR_INFO, oRequestFileSystemItem.sWindowsPath,
        COLOR_NORMAL, " could not be parsed.",
      );
      oConsole.fOutput(
        COLOR_NORMAL, "  ",
        COLOR_INFO, oException.sMessage,
      );
      for (sName, xValue) in oException.dxDetails.items():
        oConsole.fOutput(
          COLOR_NORMAL, "  ",
          COLOR_LIST, CHAR_LIST,
          COLOR_NORMAL, " ",
          COLOR_INFO, sName,
          COLOR_NORMAL, " = ",
          COLOR_INFO, str(xValue),
        );
      sys.exit(guExitCodeBadArgument);
    if fbIsProvided(sbzHTTPVersion):
      oRequest.sbHTTPVersion = sbzHTTPVersion;
    if fbIsProvided(sbzMethod):
      oRequest.sbMethod = sbzMethod;
    # When setting the body, we automatically set the `Content-Length` header.
    # This can be removed or modified using the header arguments immediately after
    if sx0Body is not None:
      fApplyBodyToRequest(
        oRequest = oRequest,
        sxBody = sx0Body,
        bCompress = bCompressBody,
        bApplyChunkedEncoding = bApplyChunkedEncodingToBody,
        bSetContentLengthHeader = bSetContentLengthHeaderForBody,
      );
    # Apply header arguments:
    fApplyHeaderSettingsToRequest(
      asbRemoveHeadersForLowerNames = asbRemoveHeadersForLowerNames,
      dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbReplaceHeaderNameAndValue_by_sLowerName,
      atsbAddHeadersNameAndValue = atsbAddHeadersNameAndValue,
      oRequest = oRequest,
    );
    if o0URL is None:
      s0Extension = oRequestFileSystemItem.s0Extension.lower() if oRequestFileSystemItem.s0Extension else None;
      if s0Extension not in ["http", "https"]:
        oConsole.fOutput(
          COLOR_ERROR,  CHAR_ERROR,
          COLOR_NORMAL, " Cannot determine the protocol to use because the HTTP request input file does",
        );
        oConsole.fOutput(
          "  not have a .http(s) extension and no URL was provided.",
        );
        sys.exit(guExitCodeBadArgument);
      sbProtocol = bytes(ord(s) for s in s0Extension);
      aoHostHeaders = oRequest.oHeaders.faoGetForNormalizedName(b"Host");
      if len(aoHostHeaders) == 0:
        oConsole.fOutput(
          COLOR_ERROR,  CHAR_ERROR,
          COLOR_NORMAL, " Cannot determine the server to connect to because the HTTP request input file",
        );
        oConsole.fOutput(
          "  does not contain a 'Host' header and no URL was provided.",
        );
        sys.exit(guExitCodeBadArgument);
      elif len(aoHostHeaders) > 1 and len(set([oHostHeader.sbNormalizedValue for oHostHeader in aoHostHeaders])) > 1:
        oConsole.fOutput(
          COLOR_WARNING,  CHAR_WARNING,
          COLOR_NORMAL,   " Selected the server name found in the first Host header out of ",
          COLOR_INFO,     str(len(aoHostHeaders)),
          COLOR_NORMAL,   "."
        );
      sbURL = b"%s://%s%s" % (
        sbProtocol,
        aoHostHeaders[0].sbValue,
        oRequest.sbURL,
      );
      oURL = cURL.foFromBytesString(sbURL);
    else:
      oURL = o0URL;
    o0Request = oRequest;
  elif o0URL:
    oURL = o0URL;
    o0Request = None;
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
  oClient = foGetClient(
    bUseProxy = bUseProxy,
    o0ProxyServerURL = o0ProxyServerURL,
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
    if oClient.o0CookieStore and o0Request:
      oClient.o0CookieStore.fApplyToRequestForURL(o0Request, oURL);
    
    if bProcessM3UFile:
      assert not o0Request; # This should have been prevented when parsing the arguments.
      ### M3U ######################################################################
      fProcessM3UFile(
        oClient = oClient,
        oURL = oURL,
        sbzHTTPVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        sx0Body = sx0Body,
        bAddContentLengthHeaderForBody = bAddContentLengthHeaderForBody,
        bApplyChunkedEncodingToBody = bApplyChunkedEncodingToBody,
        bCompressBody = bCompressBody,
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
      assert not o0Request; # This should have been prevented when parsing the arguments.
      ### SEGMENTED VIDEO ##########################################################
      # Multiple request to URL with increasing index until we get a response that is not "200 Ok"
      fProcessSegmentedVideo(
        oClient = oClient,
        oURL = oURL,
        sbzHTTPVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        sx0Body = sx0Body,
        bAddContentLengthHeaderForBody = bAddContentLengthHeaderForBody,
        bApplyChunkedEncodingToBody = bApplyChunkedEncodingToBody,
        bCompressBody = bCompressBody,
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
    elif o0Request is None:
      ### URL ######################################################################
      # Single request from URL
      foGetResponseForURL(
        oClient = oClient,
        oURL = oURL,
        sbzHTTPVersion = sbzHTTPVersion,
        sbzMethod = sbzMethod,
        sx0Body = sx0Body,
        bAddContentLengthHeaderForBody = bAddContentLengthHeaderForBody,
        bApplyChunkedEncodingToBody = bApplyChunkedEncodingToBody,
        bCompressBody = bCompressBody,
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
        oClient = oClient,
        oRequest = o0Request,
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
    oClient.fStop();