"""                                                    _   _                  
           ┄┄┄┄┄┄┄┄╒╦╦┄┄╦╦╕┄╒═╦╦═╕┄╒═╦╦═╕┄╒╦╦══╦╗┄┄▄┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄          
                    ║╠══╣║    ║║     ║║    ║╠══╩╝    ╱╱  ╱╱                   
         ┄┄┄┄┄┄┄┄┄┄╘╩╩┄┄╩╩╛┄┄╘╩╩╛┄┄┄╘╩╩╛┄┄╘╩╩╛┄┄┄┄▀┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄            
                                                    ‾   ‾                  """;
import base64, os, re, sys, urllib;

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
  from mHTTPProtocol import (
    cInvalidURLException,
    cURL,
    fsb0GetMediaTypeForExtension,
  );
  from mNotProvided import (
    fbIsProvided,
    zNotProvided
  );
  try: # mSSL support is optional
    import mSSL as m0SSL;
  except ModuleNotFoundError as oException:
    if oException.args[0] != "No module named 'mSSL'":
      raise;
    m0SSL = None;
  
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from faxListOutput import faxListOutput;
  from foConsoleLoader import foConsoleLoader;
  from fOutputExceptionAndExit import fOutputExceptionAndExit;
  from fOutputUsageInformation import fOutputUsageInformation;
  from fsbEncodeHTMLEntities import fsbEncodeHTMLEntities;
  from mColorsAndChars import (
    COLOR_ERROR, CHAR_ERROR,
    COLOR_HILITE,
    COLOR_INFO, 
    COLOR_LIST, CHAR_LIST,
    COLOR_NORMAL
  );
  from mExitCodes import (
    guExitCodeBadArgument,
    guExitCodeCannotReadRequestBodyFromFile,
    guExitCodeSuccess,
  );
  from mRunAsClient import fRunAsClient;
  from mRunAsServer import fRunAsServer;
  oConsole = foConsoleLoader();

  if __name__ != "__main__":
    sys.exit(0);
  if len(sys.argv) == 1:
    fOutputUsageInformation(bOutputAllOptions = False);
    sys.exit(guExitCodeSuccess);
  
  rURL = re.compile(r"^https?://.*$", re.I);
  rMethod = re.compile(r"^[A-Z]+$", re.I);
  rHTTPVersion = re.compile(r"^HTTP\/\d+\.\d+$", re.I);
  rCharEncoding = re.compile(r"([^\\]+)|\\(?:x([0-9a-f]{2}))?", re.I);
  
  asArguments = sys.argv[1:];
  # We track which arguments apply to which "run as type" (client/server/proxy)
  # so if the user provides arguments that would require us to run as two different
  # types we can show them an error that explains which arguments are the cause of this.
  asRunAsClientArguments = [];
  asRunAsServerArguments = [];
  asRunAsProxyArguments = [];
  
  asbClientShouldRemoveHeadersForLowerNames = [];
  bClientShouldDownloadToFile = False;
  bClientShouldProcessM3UFile = False;
  bClientShouldProcessSegmentedM3U = False;
  bClientShouldProcessSegmentedVideo = None;
  bClientShouldSaveCookieStore = False;
  bClientShouldSaveHTTPResponsesToFiles = False;
  bClientShouldUseProxy = False;
  bDecodeBodyOfHTTPMessages = False;
  bFailOnDecodeBodyErrors = False;
  bForceHexOutputOfHTTPMessageBody = False;
  bRunAsServer = False;
  bzSecureConnections = zNotProvided;
  bzShowMessageBody = zNotProvided;
  bzShowProgress = zNotProvided;
  bzShowRequest = zNotProvided;
  bzShowResponse = zNotProvided;
  bzShowDetails = zNotProvided;
  d0ClientShouldSetForm_sValue_by_sName = None;
  d0ClientShouldSetJSON_sValue_by_sName = None;
  d0ClientShouldSetFormData_dxValue_by_sName = None;
  dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName = {};
  atsbClientShouldAddHeadersNameAndValue = [];
  dsbSpoofedHost_by_sbHost = {};
  n0zTimeoutInSeconds = zNotProvided;
  nSendDelayPerByteInSeconds = 0;
  o0ClientShouldDownloadToFileSystemItem = None;
  o0ClientShouldUseCookieStoreJSONFileSystemItem = None;
  o0ClientShouldUseHTTPProxyServerURL = None;
  o0ClientShouldUseNetscapeCookiesFileSystemItem = None;
  o0ClientShouldUseURL = None;
  o0InputFileSystemItem = None;
  o0SaveHTTPResponsesToFileSystemItem = None;
  sx0ClientShouldUseBody = None;
  bClientShouldCompressBody = True;
  bClientShouldApplyChunkedEncodingToBody = True;
  bClientShouldAddContentLengthHeaderForBody = True;
  sbzServerShouldUseHost = zNotProvided;
  sbzHTTPVersion = zNotProvided;
  sbzClientShouldUseMethod = zNotProvided;
  u0ClientShouldUseMaxRedirects = None;
  uzServerShouldUsePortNumber = zNotProvided;
  uHexOutputCharsPerLine = 16;
  osProvidedArgumentsThatSetBody = set();

  for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
    def fsUnescape(sValue):
      return "".join([
          (
            oMatch.group(1) if oMatch.group(1) else 
            chr(int(oMatch.group(2), 16)) if oMatch.group(2) else
            ""
          )
          for oMatch in rCharEncoding.finditer(sValue)
        ]);
    def ts0SplitAndUnescape(sValue, sSeparator):
      if sValue == "":
        return (None, None);
      tsComponents = sValue.split(sSeparator, 1);
      if len(tsComponents) == 1:
        return (
          fsUnescape(sValue),
          None
        );
      return (
        fsUnescape(tsComponents[0]),
        fsUnescape(tsComponents[1]),
      );
    def fbGetBooleanArgumentValue():
      sValue = fsUnescape(s0Value or "").lower();
      if sValue in ["", "true"]:
        return True;
      if s0Value == "false":
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
    def fsbConvertToBytes(sValue):
      auBytes = [ord(s) for s in sValue];
      uBadCharsCount = False;
      for uIndex in range(len(auBytes)):
        if auBytes[uIndex] > 255:
          uBadCharsCount += 1;
          if uBadCharsCount == 1:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " You must provide an ASCII value for \"",
              COLOR_INFO, sArgument,
              COLOR_NORMAL, "\".",
            );
          if uBadCharsCount < 4:
            oConsole.fOutput(
              COLOR_NORMAL, "  • Character #",
              COLOR_INFO, str(uIndex),
              COLOR_NORMAL, " (",
              COLOR_INFO, repr(sValue[uIndex]),
              COLOR_NORMAL, ") is not an ASCII character.",
            );
      if uBadCharsCount > 3:
        oConsole.fOutput(
          COLOR_NORMAL, "  ...and ", str(uBadCharsCount), " more characters.",
        );
        sys.exit(guExitCodeBadArgument);
      return bytes(auBytes);
    def fRequiredArgumentValue():
      if s0Value: return;
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " You must provide a value for \"",
        COLOR_INFO, sArgument,
        COLOR_NORMAL, "\".",
      );
      sys.exit(guExitCodeBadArgument);
    if not s0LowerName:
      sUnescapedArgument = fsUnescape(sArgument);
      if o0ClientShouldUseURL is None and rURL.match(sUnescapedArgument):
        asRunAsClientArguments.append(sArgument);
        try:
          o0ClientShouldUseURL = cURL.foFromBytesString(
            fsbConvertToBytes(sUnescapedArgument),
            # We're not picky: we want to allow going outside the protocol:
            bAllowInvalidURLs = True,
          );
        except cInvalidURLException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" is not a valid URL.",
          );
          sys.exit(guExitCodeBadArgument);
      elif not fbIsProvided(sbzClientShouldUseMethod) and rMethod.match(sUnescapedArgument):
        asRunAsClientArguments.append(sArgument);
        sbzClientShouldUseMethod = fsbConvertToBytes(sUnescapedArgument);
      elif rHTTPVersion.match(sUnescapedArgument):
        sbzHTTPVersion = fsbConvertToBytes(sUnescapedArgument);
      elif o0InputFileSystemItem:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Superfluous argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      elif not cFileSystemItem.fbIsValidPath(sArgument):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Unrecognized argument \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\".",
          );
          oConsole.fOutput(
            COLOR_NORMAL, "  It is neither a HTTP method, version, URL or a valid file/folder path.",
          );
          sys.exit(guExitCodeBadArgument);
      else:
        o0InputFileSystemItem = cFileSystemItem(sArgument);
        if not o0InputFileSystemItem.fbExists():
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Unrecognized argument \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\".",
          );
          oConsole.fOutput(
            COLOR_NORMAL, "  It is neither a HTTP method, version, URL or an existing file/folder.",
          );
          sys.exit(guExitCodeBadArgument);
        else:
          if bClientShouldProcessM3UFile:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " You cannot use a HTTP request file as input and process a .m3u file response at the same time.",
            );
            sys.exit(guExitCodeBadArgument);
          if bClientShouldProcessSegmentedVideo:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " You cannot use a HTTP request file as input and process a segmented video response at the same time.",
            );
            sys.exit(guExitCodeBadArgument);
    ############################################################################
    elif s0LowerName in ["bl", "basic-login"]:
      asRunAsClientArguments.append(sArgument);
      sbBase64EncodedUserNameColonPassword = base64.b64encode(
        fsbConvertToBytes(fsUnescape(s0Value or ""))
      );
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"authorization"] = (
        b"Authorization",
        b"basic %s" % sbBase64EncodedUserNameColonPassword
      );
    ############################################################################
    elif s0LowerName in ["c", "cookies", "netscape-cookies"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      o0ClientShouldUseNetscapeCookiesFileSystemItem = cFileSystemItem(s0Value);
      if not o0ClientShouldUseNetscapeCookiesFileSystemItem.fbIsFile():
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot find file \"",
          COLOR_INFO, o0ClientShouldUseNetscapeCookiesFileSystemItem.sPath,
          COLOR_NORMAL, "\"."
        );
        sys.exit(guExitCodeBadArgument);
    ############################################################################
    elif s0LowerName in ["cs", "cookie-store"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldSaveCookieStore = True;
      if s0Value:
        o0ClientShouldUseCookieStoreJSONFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["body"]:
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      sx0ClientShouldUseBody = fsbConvertToBytes(fsUnescape(s0Value or ""));
      # We are adding a raw body; don't apply compression or chunked encoding
      bClientShouldCompressBody = False;
      bClientShouldApplyChunkedEncodingToBody = False;
    ############################################################################
    elif s0LowerName in ["bf", "body-file"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      oDataFileSystemItem = cFileSystemItem(s0Value);
      if not oDataFileSystemItem.fbIsFile():
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot find file \"",
          COLOR_INFO, oDataFileSystemItem.sPath,
          COLOR_NORMAL, "\"."
        );
        sys.exit(guExitCodeBadArgument);
      try:
        sx0ClientShouldUseBody = oDataFileSystemItem.fsbRead();
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot read from file ",
          COLOR_INFO, oDataFileSystemItem.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
      # We are adding a raw body; don't apply compression or chunked encoding
      bClientShouldCompressBody = False;
      bClientShouldApplyChunkedEncodingToBody = False;
    ############################################################################
    elif s0LowerName in ["data"]:
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      sx0ClientShouldUseBody = fsUnescape(s0Value or "");
    ############################################################################
    elif s0LowerName in ["df", "data-file"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      oDataFileSystemItem = cFileSystemItem(s0Value);
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
        sx0ClientShouldUseBody = str(sbFileContent, "utf-8", "strict");
      except UnicodeDecodeError as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot decode file content as UTF-8: ",
          COLOR_INFO, oException.reason,
          COLOR_NORMAL, ".",
        );
        sys.exit(guExitCodeCannotReadRequestBodyFromFile);
    ############################################################################
    elif s0LowerName in ["debug"]:
      if fbGetBooleanArgumentValue():
        if not m0DebugOutput:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The ",
            COLOR_INFO, "mDebugOutput",
            COLOR_NORMAL, " module is needed to show debug information but it is not available!",
          );
          sys.exit(guExitCodeBadArgument);
        m0DebugOutput.fEnableAllDebugOutput();
    ############################################################################
    elif s0LowerName in ["db", "decode", "decode-body"]:
      bDecodeBodyOfHTTPMessages = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["fail-on-decode-errors", "report-decode-body-errors"]:
      bFailOnDecodeBodyErrors = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["dl", "download"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldDownloadToFile = True;
      if s0Value:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["form"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sName, sValue = ts0SplitAndUnescape(s0Value, "=");
      # We accept multiple copies of this argument with different values.
      osProvidedArgumentsThatSetBody.add(f"--{s0LowerName}=...");
      if d0ClientShouldSetForm_sValue_by_sName is None:
        d0ClientShouldSetForm_sValue_by_sName = {};
      d0ClientShouldSetForm_sValue_by_sName[sName] = sValue;
    ############################################################################
    elif s0LowerName in ["form-data"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sName, sValue = ts0SplitAndUnescape(s0Value, "=");
      if d0ClientShouldSetForm_sValue_by_sName is None:
        d0ClientShouldSetForm_sValue_by_sName = {};
      d0ClientShouldSetForm_sValue_by_sName[sName] = sValue;
      # We accept multiple copies of this argument with different values.
      osProvidedArgumentsThatSetBody.add(f"--{s0LowerName}=...");
      if d0ClientShouldSetFormData_dxValue_by_sName is None:
        d0ClientShouldSetFormData_dxValue_by_sName = {};
      sbName = fsbEncodeHTMLEntities(sName);
      sbValue = fsbEncodeHTMLEntities(sValue);
      d0ClientShouldSetFormData_dxValue_by_sName[sbName] = {
        "sbValue": sbValue,
      };
    ############################################################################
    elif s0LowerName in ["form-data-upload"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      # Only the name must be un-escaped, so we cannot use `ts0SplitAndUnescape`
      tsSplitNameAndFilePath = s0Value.split("=", 1);
      if len(tsSplitNameAndFilePath) != 2:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " You must provide a value with the format \"",
          COLOR_INFO, "name=<path to file>",
          COLOR_NORMAL, "\" for the argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      sName, sFilePath = tsSplitNameAndFilePath;
      sName = fsUnescape(sName);
      oUploadFileSystemItem = cFileSystemItem(sFilePath);
      if not oUploadFileSystemItem.fbIsFile():
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot find file \"",
          COLOR_INFO, oUploadFileSystemItem.sPath,
          COLOR_NORMAL, "\"."
        );
        sys.exit(guExitCodeBadArgument);
      try:
        sbValue = oUploadFileSystemItem.fsbRead();
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot read from file ",
          COLOR_INFO, oUploadFileSystemItem.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
      if d0ClientShouldSetFormData_dxValue_by_sName is None:
        d0ClientShouldSetFormData_dxValue_by_sName = {};
      sbName = fsbEncodeHTMLEntities(sName);
      sbFileName = fsbEncodeHTMLEntities(os.path.split(sFilePath)[1]);
      d0ClientShouldSetFormData_dxValue_by_sName[sbName] = {
        "sbFileName": sbFileName,
        "sbContentType": b"application/octet-stream",
        "sbValue": sbValue,
      };
    ############################################################################
    elif s0LowerName in ["header"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sName, sValue = ts0SplitAndUnescape(s0Value, ":");
      sbHeaderName = fsbConvertToBytes(sName);
      sbHeaderValue = fsbConvertToBytes(sValue);
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[sbHeaderName.lower()] = (sbHeaderName, sbHeaderValue);
    ############################################################################
    elif s0LowerName in ["header-"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sbHeaderName = fsbConvertToBytes(fsUnescape(s0Value));
      asbClientShouldRemoveHeadersForLowerNames.append(sbHeaderName.lower());
    ############################################################################
    elif s0LowerName in ["header+"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sbValue = fsbConvertToBytes(fsUnescape(s0Value));
      sName, sValue = ts0SplitAndUnescape(s0Value, ":");
      sbHeaderName = fsbConvertToBytes(sName);
      sbHeaderValue = fsbConvertToBytes(sValue);
      atsbClientShouldAddHeadersNameAndValue.append((sbHeaderName, sbHeaderValue));
    ############################################################################
    elif s0LowerName in ["hex", "hex-output", "hex-output-body"]:
      bForceHexOutputOfHTTPMessageBody = True;
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
    ############################################################################
    elif s0LowerName in ["h", "host", "hostname"]:
      fRequiredArgumentValue();
      if fbIsProvided(sbzServerShouldUseHost):
        oConsole.fOutput(
          "A ",
          COLOR_INFO, "host",
          COLOR_NORMAL, " can only be provided once!",
        );
        sys.exit(guExitCodeBadArgument);
      sbzServerShouldUseHost = fsbConvertToBytes(fsUnescape(s0Value));
    ############################################################################
    elif s0LowerName in ["json"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sName, sValue = ts0SplitAndUnescape(s0Value, ":");
      if d0ClientShouldSetJSON_sValue_by_sName is None:
        d0ClientShouldSetJSON_sValue_by_sName = {};
      d0ClientShouldSetJSON_sValue_by_sName[sName] = sValue;
      # We accept multiple copies of this argument with different values.
      osProvidedArgumentsThatSetBody.add(f"--{s0LowerName}=...");
    elif s0LowerName in ["json-file"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      # We accept two exactly the same copies of this argument but not two with
      # different values.
      osProvidedArgumentsThatSetBody.add(sArgument);
      oJSONFileSystemItem = cFileSystemItem(s0Value);
      if not oJSONFileSystemItem.fbIsFile():
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot find file \"",
          COLOR_INFO, oJSONFileSystemItem.sPath,
          COLOR_NORMAL, "\"."
        );
        sys.exit(guExitCodeBadArgument);
      try:
        sbFileContent = oJSONFileSystemItem.fsbRead();
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot read from file ",
          COLOR_INFO, oJSONFileSystemItem.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
      try:
        sx0ClientShouldUseBody = str(sbFileContent, "utf-8", "strict");
      except UnicodeDecodeError as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot decode file content as UTF-8: ",
          COLOR_INFO, oException.reason,
          COLOR_NORMAL, ".",
        );
        sys.exit(guExitCodeCannotReadRequestBodyFromFile);
      if (
        b"content-type" not in dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName
      ):
        dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"content-type"] = (b"Content-Type", b"application/json");
    ############################################################################
    elif s0LowerName in ["m3u"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldProcessM3UFile = True;
      bClientShouldDownloadToFile = True;
      # If a path is provided for downloading, set it.
      if s0Value is not None:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["sm3u", "segmented-m3u"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldProcessM3UFile = True;
      bClientShouldDownloadToFile = True;
      bClientShouldProcessSegmentedM3U = True;
      if s0Value is not None:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["p", "port", "port-number"]:
      asRunAsServerArguments.append(sArgument);
      if fbIsProvided(uzServerShouldUsePortNumber):
        oConsole.fOutput(
          "A ",
          COLOR_INFO, "port number",
          COLOR_NORMAL, " can only be provided once!",
        );
        sys.exit(guExitCodeBadArgument);
      if s0Value:
        try:
          uzServerShouldUsePortNumber = int(s0Value);
          assert 0 < uzServerShouldUsePortNumber < 0x10000;
        except:
          oConsole.fOutput(
            "The ",
            COLOR_INFO, s0LowerName,
            COLOR_NORMAL, " argument must contain a valid port number (1-65535)!",
          );
          sys.exit(guExitCodeBadArgument);
      else:
        uzServerShouldUsePortNumber = zNotProvided;
    ############################################################################
    elif s0LowerName in ["media-type", "mime-type"]:
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sValue = fsUnescape(s0Value or "");
      if sValue.startswith("."):
        sb0MediaType = fsb0GetMediaTypeForExtension(sValue);
        if not sb0MediaType:
          oConsole.fOutput(
            "The media type for file extension ",
            COLOR_INFO, sValue,
            COLOR_NORMAL, " is not known.",
          );
          sys.exit(guExitCodeBadArgument);
        sbMediaType = sb0MediaType;
      else:
        try:
          sbMediaType = sValue(s0Value, "ascii", "strict");
        except:
          oConsole.fOutput(
            "The ",
            COLOR_INFO, s0LowerName,
            COLOR_NORMAL, " argument must contain a valid host.",
          );
          sys.exit(guExitCodeBadArgument);
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"content-type"] = (b"Content-Type", sbMediaType);
    ############################################################################
    elif s0LowerName in ["proxy", "http-proxy"]:
      asRunAsClientArguments.append(sArgument);
      if bClientShouldUseProxy:
        if o0ClientShouldUseHTTPProxyServerURL is not None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " You can only provide one proxy argument.",
          );
          sys.exit(guExitCodeBadArgument);
      bClientShouldUseProxy = True;
      if s0Value:
        o0ClientShouldUseHTTPProxyServerURL = cURL.foFromBytesString(
          fsbConvertToBytes(fsUnescape(s0Value or ""))
          # Here we are picky: we want the URL to be valid, so we can talk to
          # the proxy.
        );
    ############################################################################
    elif s0LowerName in ["r", "max-redirects", "follow-redirects"]:
      asRunAsClientArguments.append(sArgument);
      if s0Value:
        try:
          u0ClientShouldUseMaxRedirects = int(s0Value);
          assert u0ClientShouldUseMaxRedirects >= 0, "";
        except:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value for \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" must be a positive integer number or zero.",
          );
          sys.exit(guExitCodeBadArgument);
      else:
        u0ClientShouldUseMaxRedirects = 32;
    ############################################################################
    elif s0LowerName in ["save", "save-response", "save-responses"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldSaveHTTPResponsesToFiles = True;
      if s0Value:
        o0SaveHTTPResponsesToFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["s", "srv", "serve", "server",]:
      asRunAsServerArguments.append(sArgument);
      bRunAsServer = True;
    ############################################################################
    elif s0LowerName in ["secure"]:
      bzSecureConnections = fbGetBooleanArgumentValue();
      if bzSecureConnections and not m0SSL:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " The value for \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\" requires that mSSL is available but it is not.",
        );
        sys.exit(guExitCodeBadArgument);
    ############################################################################
    elif s0LowerName in ["insecure", "non-secure"]:
      asRunAsClientArguments.append(sArgument);
      bzSecureConnections = not fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["sv", "segmented-video"]:
      asRunAsClientArguments.append(sArgument);
      bClientShouldProcessSegmentedVideo = True;
      bClientShouldDownloadToFile = True;
      # If a path is provided for downloading, set it. If not, make sure we download by setting it to None
      if s0Value:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    ############################################################################
    elif s0LowerName in ["send-delay"]:
      if s0Value is None or s0Value.lower() == "none":
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " You must provide a number larger than or equal to zero as a value for \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      else:
        try:
          nSendDelayPerByteInSeconds = float(s0Value);
          assert nSendDelayPerByteInSeconds >= 0, "";
        except:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value for \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" must be a number larger than or equal to zero.",
          );
          sys.exit(guExitCodeBadArgument);
    ############################################################################
    elif s0LowerName in ["show-details"]:
      bzShowDetails = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["show-body", "show-message-body"]:
      bzShowMessageBody = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["show-progress"]:
      bzShowProgress = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["show-request"]:
      bzShowRequest = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName in ["show-response"]:
      bzShowResponse = fbGetBooleanArgumentValue();
    ############################################################################
    elif s0LowerName.startswith("spoof:"):
      fRequiredArgumentValue();
      asRunAsClientArguments.append(sArgument);
      sbHost = fsbConvertToBytes(fsUnescape(s0LowerName.split(":", 1)[1]));
      sbIPaddress = fsbConvertToBytes(fsUnescape(s0Value or ""));
      dsbSpoofedHost_by_sbHost[sbHost] = sbIPaddress;
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
    else:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Unknown argument \"",
        COLOR_INFO, sArgument,
        COLOR_NORMAL, "\".",
      );
      sys.exit(guExitCodeBadArgument);

  # Make sure we are not being asked to run as a client, server, and proxy at the same time:
  asRunAsTypes = [];
  asArgumentsForClientNotUsedByOtherTypes = [
    sArgument for sArgument in asRunAsClientArguments if sArgument not in asRunAsServerArguments + asRunAsProxyArguments
  ];
  if len(asArgumentsForClientNotUsedByOtherTypes) > 0:
    asRunAsTypes.append("client");
  asArgumentsForServerNotUsedByOtherTypes = [
    sArgument for sArgument in asRunAsServerArguments if sArgument not in asRunAsClientArguments + asRunAsProxyArguments
  ];
  if len(asArgumentsForServerNotUsedByOtherTypes) > 0:
    asRunAsTypes.append("server");
  asArgumentsForProxyNotUsedByOtherTypes = [
    sArgument for sArgument in asRunAsProxyArguments if sArgument not in asRunAsClientArguments + asRunAsServerArguments
  ];
  if len(asArgumentsForProxyNotUsedByOtherTypes) > 0:
    asRunAsTypes.append("proxy");
  if not asRunAsTypes:
    print("args: %s" % repr(sys.argv[1:]));
    print("client args: %s" % repr(asRunAsClientArguments));
    if asRunAsClientArguments: print("  not used by others: %s" % repr(asArgumentsForClientNotUsedByOtherTypes));
    print("server args: %s" % repr(asRunAsServerArguments));
    if asRunAsServerArguments: print("  not used by others: %s" % repr(asArgumentsForServerNotUsedByOtherTypes));
    print("proxy args: %s" % repr(asRunAsProxyArguments));
    if asRunAsProxyArguments: print("  not used by others: %s" % repr(asArgumentsForProxyNotUsedByOtherTypes));
  assert len(asRunAsTypes) > 0, \
      "For unknown reasons it appears we do not know what to do!?";
  if len(asRunAsTypes) > 1:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " This script cannot run as ",
      faxListOutput(asRunAsTypes, "and"),
      COLOR_NORMAL, " at the same time.",
    );
    for (sRunAsType, asArgumentsNotUsedByOtherTypes) in (
      ("client", asArgumentsForClientNotUsedByOtherTypes),
      ("server", asArgumentsForServerNotUsedByOtherTypes),
      ("proxy", asArgumentsForProxyNotUsedByOtherTypes),
    ):
      if (asArgumentsNotUsedByOtherTypes):
        oConsole.fOutput(
          COLOR_NORMAL, "  These arguments indicate you want the script to run as a ",
          COLOR_INFO, sRunAsType,
          COLOR_NORMAL, ":",
        );
        oConsole.fOutput(
          COLOR_NORMAL, "    ",
          COLOR_INFO, asArgumentsNotUsedByOtherTypes,
        );
    oConsole.fOutput(
      COLOR_NORMAL, "  Please try using arguments that apply only to a client, server, or proxy.",
    );
    sys.exit(guExitCodeBadArgument);
  sRunAs = asRunAsTypes[0];
  # If not explicitly set, show progress
  bShowProgress = bzShowProgress if fbIsProvided(bzShowProgress) else True;
  # If not explicitly set, only show requests and responses when we are not downloading.
  bShowRequestResponseDefault = (
    not (bClientShouldDownloadToFile or bClientShouldSaveHTTPResponsesToFiles)
  ) if sRunAs == "client" else (
    True
  );
  bShowMessageBody = bzShowMessageBody if fbIsProvided(bzShowMessageBody) else True;
  bShowRequest = bzShowRequest if fbIsProvided(bzShowRequest) else bShowRequestResponseDefault;
  bShowResponse = bzShowResponse if fbIsProvided(bzShowResponse) else bShowRequestResponseDefault;
  bShowDetails = bzShowDetails if fbIsProvided(bzShowDetails) else True;

  if sRunAs == "client":
    # We have multiple arguments that can set the request body but we can only
    # use one at a time. Check that the user did not provide multiple values.
    if len(osProvidedArgumentsThatSetBody) > 1:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " The following arguments cannot be provided simultaneously: ",
      );
      for sArgument in sorted(osProvidedArgumentsThatSetBody, key=lower):
        oConsole.fOutput(
          COLOR_NORMAL, " ",
          COLOR_LIST, CHAR_LIST,
          COLOR_NORMAL, " ",
          COLOR_HILITE, sArgument,
        );
      oConsole.fOutput(
        COLOR_NORMAL, "  The request body can only be set through one of these arguments.",
      );
      sys.exit(guExitCodeBadArgument);
      
    if d0ClientShouldSetFormData_dxValue_by_sName is not None:
      sbBoundary = b"-".join([b"BOUNDARY"] * 5);
      sbData = b"";
      for (sbName, dxValue) in d0ClientShouldSetFormData_dxValue_by_sName.items():
        sbData += b"--%s\r\n" % (sbBoundary,);
        
        sbContentDisposition = b"form-data; name=\"%s\"" % (sbName,);
        if "sbFilePath" in dxValue:
          sbContentDisposition += b"; filename=\"%s\"" % (dxValue["sbFileName"],);
        sbData += b"Content-Disposition: %s\r\n" % sbContentDisposition;
        
        if "sbContentType" in dxValue:
          sbData += b"Content-Type: %s\r\n" % (sbContentType,);
        sbData += b"\r\n";
        sbData += b"%s\r\n" % dxValue["sbValue"];
      
      sbData += b"--%s--\r\n" % (sbBoundary,),
      if (
        b"content-type" not in dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName
      ):
        dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"content-type"] = (
          b"Content-Type",
          b"multipart/form-data; boundary=%s" % sbBoundary
        );
      sx0ClientShouldUseData = sbData;
    
    fRunAsClient(
      bAddContentLengthHeaderForBody = bClientShouldAddContentLengthHeaderForBody,
      bCompressBody = bClientShouldCompressBody,
      bApplyChunkedEncodingToBody = bClientShouldApplyChunkedEncodingToBody,
      bDecodeBodyOfHTTPMessages = bDecodeBodyOfHTTPMessages,
      bDownloadToFile = bClientShouldDownloadToFile,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bForceHexOutputOfHTTPMessageBody = bForceHexOutputOfHTTPMessageBody,
      bProcessM3UFile = bClientShouldProcessM3UFile,
      bProcessSegmentedM3U = bClientShouldProcessSegmentedM3U,
      bProcessSegmentedVideo = bClientShouldProcessSegmentedVideo,
      bSaveCookieStore = bClientShouldSaveCookieStore,
      bSaveHTTPResponsesToFiles = bClientShouldSaveHTTPResponsesToFiles,
      bShowDetails = bShowDetails,
      bShowMessageBody = bShowMessageBody,
      bShowProgress = bShowProgress,
      bShowRequest = bShowRequest,
      bShowResponse = bShowResponse,
      bUseProxy = bClientShouldUseProxy,
      bVerifyCertificates = False if bzSecureConnections is False else True, # default to secure connections
      d0SetForm_sValue_by_sName = d0ClientShouldSetForm_sValue_by_sName,
      d0SetJSON_sValue_by_sName = d0ClientShouldSetJSON_sValue_by_sName,
      asbRemoveHeadersForLowerNames = asbClientShouldRemoveHeadersForLowerNames,
      dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName,
      atsbAddHeadersNameAndValue = atsbClientShouldAddHeadersNameAndValue,
      dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
      n0zTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      o0CookieStoreJSONFileSystemItem = o0ClientShouldUseCookieStoreJSONFileSystemItem,
      o0DownloadToFileSystemItem = o0ClientShouldDownloadToFileSystemItem,
      o0RequestFileSystemItem = o0InputFileSystemItem,
      o0ProxyServerURL = o0ClientShouldUseHTTPProxyServerURL,
      o0NetscapeCookiesFileSystemItem = o0ClientShouldUseNetscapeCookiesFileSystemItem,
      o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
      o0URL = o0ClientShouldUseURL,
      sx0Body = sx0ClientShouldUseBody,
      sbzHTTPVersion = sbzHTTPVersion,
      sbzMethod = sbzClientShouldUseMethod,
      u0MaxRedirects = u0ClientShouldUseMaxRedirects,
      uHexOutputCharsPerLine = uHexOutputCharsPerLine,
    );
  elif sRunAs == "server":
    fRunAsServer(
      bDecodeBodyOfHTTPMessages = bDecodeBodyOfHTTPMessages,
      bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
      bForceHexOutputOfHTTPMessageBody = bForceHexOutputOfHTTPMessageBody,
      bSecureConnections = True if bzSecureConnections is True else False, # default to insecure connections.
      bShowDetails = bShowDetails,
      bShowMessageBody = bShowMessageBody,
      bShowProgress = bShowProgress,
      bShowRequest = bShowRequest,
      bShowResponse = bShowResponse,
      n0zTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      o0BaseFolderFileSystemItem = o0InputFileSystemItem,
      sbzHost = sbzServerShouldUseHost,
      uHexOutputCharsPerLine = uHexOutputCharsPerLine,
      uzPortNumber = uzServerShouldUsePortNumber,      
    );
  elif sRunAs == "proxy":
    raise NotImplementedError();
  sys.exit(guExitCodeSuccess);
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;