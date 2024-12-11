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
  from mHTTPProtocol import (
    cHTTPInvalidURLException,
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
  from mRunAsClient import fRunAsClient;
  from mRunAsServer import fRunAsServer;
  oConsole = foConsoleLoader();

  if __name__ != "__main__":
    sys.exit(0);
  if len(sys.argv) == 1:
    fOutputUsageInformation(bOutputAllOptions = False);
    sys.exit(guExitCodeSuccess);
  
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
  asbClientShouldRemoveHeadersForLowerNames = [];
  dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName = {};
  atsbClientShouldAddHeadersNameAndValue = [];
  dsbSpoofedHost_by_sbHost = {};
  d0ClientShouldSetForm_sValue_by_sName = None;
  n0zTimeoutInSeconds = zNotProvided;
  nSendDelayPerByteInSeconds = 0;
  o0ClientShouldDownloadToFileSystemItem = None;
  o0ClientShouldUseCookieStoreJSONFileSystemItem = None;
  o0ClientShouldUseHTTPProxyServerURL = None;
  o0ClientShouldUseNetscapeCookiesFileSystemItem = None;
  o0ClientShouldUseURL = None;
  o0InputFileSystemItem = None;
  o0SaveHTTPResponsesToFileSystemItem = None;
  s0ClientShouldSetHTTPRequestData = None;
  sb0ClientShouldSetHTTPRequestBody = None;
  sbzServerShouldUseHost = zNotProvided;
  sbzSetHTTPVersion = zNotProvided;
  sbzClientShouldSetMethod = zNotProvided;
  u0ClientShouldUseMaxRedirects = None;
  uzServerShouldUsePortNumber = zNotProvided;
  uHexOutputCharsPerLine = 16;

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
      if o0ClientShouldUseURL is None and rURL.match(sArgument):
        asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
        try:
          o0ClientShouldUseURL = cURL.foFromBytesString(bytes(ord(s) for s in sArgument));
        except cHTTPInvalidURLException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The value \"",
            COLOR_INFO, sArgument,
            COLOR_NORMAL, "\" is not a valid URL.",
          );
          sys.exit(guExitCodeBadArgument);
      elif not fbIsProvided(sbzClientShouldSetMethod) and rMethod.match(sArgument):
        asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
        sbzClientShouldSetMethod = bytes(ord(s) for s in sArgument);
      elif rHTTPVersion.match(sArgument):
        sbzSetHTTPVersion = bytes(ord(s) for s in sArgument);
      elif o0InputFileSystemItem:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Superfluous argument \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\".",
        );
        sys.exit(guExitCodeBadArgument);
      elif not cFileSystemItem.fbIsValidPath(sArgument) or not cFileSystemItem(sArgument).fbExists():
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
        o0InputFileSystemItem = cFileSystemItem(sArgument);
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
    elif s0LowerName in ["bl", "basic-login"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sbBase64EncodedUserNameColonPassword = base64.b64encode(bytes(ord(s) for s in (s0Value or "")));
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"authorization"] = (
        b"Authorization",
        b"basic %s" % sbBase64EncodedUserNameColonPassword
      );
    elif s0LowerName in ["c", "cookies", "netscape-cookies"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      o0ClientShouldUseNetscapeCookiesFileSystemItem = cFileSystemItem(fsRequireArgumentValue());
    elif s0LowerName in ["cs", "cookie-store"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldSaveCookieStore = True;
      if s0Value:
        o0ClientShouldUseCookieStoreJSONFileSystemItem = cFileSystemItem(s0Value);
    elif s0LowerName in ["data"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sb0ClientShouldSetHTTPRequestBody = None;
      s0ClientShouldSetHTTPRequestData = fsRequireArgumentValue();
    elif s0LowerName in ["bf", "body-file"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
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
        sb0ClientShouldSetHTTPRequestBody = oDataFileSystemItem.fsbRead();
        s0ClientShouldSetHTTPRequestData = None;
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot read from file ",
          COLOR_INFO, oDataFileSystemItem.sPath,
          COLOR_NORMAL, ".",
        );
        fOutputExceptionAndExit(oException, guExitCodeCannotReadRequestBodyFromFile);
    elif s0LowerName in ["df", "data-file"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
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
        sb0ClientShouldSetHTTPRequestBody = None;
        s0ClientShouldSetHTTPRequestData = str(sbFileContent, "utf-8", "strict");
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " File ",
          COLOR_INFO, oDataFileSystemItem.sPath,
          COLOR_NORMAL, " does not contain utf-8 encoded data.",
        );
        fOutputExceptionAndExit(oException, guExitCodeRequestDataInFileIsNotUTF8);
    elif s0LowerName in ["debug"]:
      # This argument makes sense for client, server and proxy
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
      # This argument makes sense for client, server and proxy
      bDecodeBodyOfHTTPMessages = fbParseBooleanArgument(s0Value);
    elif s0LowerName in ["fail-on-decode-errors", "report-decode-body-errors"]:
      # This argument makes sense for client, server and proxy
      bFailOnDecodeBodyErrors = fbParseBooleanArgument(s0Value);
    elif s0LowerName in ["dl", "download"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldDownloadToFile = True;
      if s0Value:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    elif s0LowerName in ["form"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sValue = fsRequireArgumentValue();
      tsFormNameAndValue = sValue.split("=", 1);
      if len(tsFormNameAndValue) == 1:
        sName = sValue; sValue = "";
      else:
        sName, sValue = tsFormNameAndValue;
      if d0ClientShouldSetForm_sValue_by_sName is None:
        d0ClientShouldSetForm_sValue_by_sName = {};
      d0ClientShouldSetForm_sValue_by_sName[sName] = sValue;
    elif s0LowerName in ["header"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sbValue = bytes(ord(s) for s in fsRequireArgumentValue());
      tsbHeaderNameAndValue = sbValue.split(b":", 1);
      if len(tsbHeaderNameAndValue) == 1:
        sbHeaderName = sbValue;
        sbHeaderValue = b"";
      else:
        sbHeaderName, sbHeaderValue = tsbHeaderNameAndValue;
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[sbHeaderName.lower()] = (sbHeaderName, sbHeaderValue);
    elif s0LowerName in ["header-"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sbHeaderName = bytes(ord(s) for s in fsRequireArgumentValue());
      asbClientShouldRemoveHeadersForLowerNames.append(sbHeaderName.lower());
    elif s0LowerName in ["header+"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sbValue = bytes(ord(s) for s in fsRequireArgumentValue());
      tsbHeaderNameAndValue = sbValue.split(b":", 1);
      if len(tsbHeaderNameAndValue) == 1:
        sbHeaderName = sbValue;
        sbHeaderValue = b"";
      else:
        sbHeaderName, sbHeaderValue = tsbHeaderNameAndValue;
      atsbClientShouldAddHeadersNameAndValue.append((sbHeaderName, sbHeaderValue));
    elif s0LowerName in ["hex", "hex-output", "hex-output-body"]:
      # This argument makes sense for client, server and proxy
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
    elif s0LowerName in ["h", "host", "hostname"]:
        if fbIsProvided(sbzServerShouldUseHost):
          oConsole.fOutput(
            "A ",
            COLOR_INFO, "host",
            COLOR_NORMAL, " can only be provided once!",
          );
          sys.exit(guExitCodeBadArgument);
        if s0Value:
          try:
            sbzServerShouldUseHost = bytes(s0Value, "ascii", "strict");
          except:
            oConsole.fOutput(
              "The ",
              COLOR_INFO, s0LowerName,
              COLOR_NORMAL, " argument must contain a valid host!",
            );
            sys.exit(guExitCodeBadArgument);
        else:
          sbzServerShouldUseHost = zNotProvided;
    elif s0LowerName in ["m3u"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldProcessM3UFile = True;
      bClientShouldDownloadToFile = True;
      # If a path is provided for downloading, set it.
      if s0Value is not None:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    elif s0LowerName in ["sm3u", "segmented-m3u"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldProcessM3UFile = True;
      bClientShouldDownloadToFile = True;
      bClientShouldProcessSegmentedM3U = True;
      if s0Value is not None:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
    elif s0LowerName in ["p", "port", "port-number"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
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
    elif s0LowerName in ["media-type", "mime-type"]:
      sExtension = fsRequireArgumentValue();
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      sb0MediaType = fsb0GetMediaTypeForExtension(sExtension);
      if not sb0MediaType:
        oConsole.fOutput(
          "The media type for ",
          COLOR_INFO, sExtension,
          COLOR_NORMAL, " is not known.",
        );
        sys.exit(guExitCodeBadArgument);
      dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName[b"content-type"] = (b"Content-Type", sb0MediaType);

      s0MediaType = s0Value;
    elif s0LowerName in ["proxy", "http-proxy"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldUseProxy = True;
      if s0Value:
        if o0ClientShouldUseHTTPProxyServerURL is not None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " You can only provide one proxy server URL.",
          );
          sys.exit(guExitCodeBadArgument);
        o0ClientShouldUseHTTPProxyServerURL = cURL.foFromBytesString(bytes(ord(s) for s in s0Value));
    elif s0LowerName in ["r", "max-redirects", "follow-redirects"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
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
    elif s0LowerName in ["save", "save-response", "save-responses"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bSaveHTTPResponsesToFiles = True;
      if s0Value:
        o0SaveHTTPResponsesToFileSystemItem = cFileSystemItem(s0Value);
    elif s0LowerName in ["s", "srv", "serve", "server",]:
      asRunAsServerArguments.append(sArgument);
      bRunAsServer = True;
    elif s0LowerName in ["secure"]:
      bzSecureConnections = fbParseBooleanArgument(s0Value);
      if bzSecureConnections and not m0SSL:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " The value for \"",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "\" requires that mSSL is available but it is not.",
        );
        sys.exit(guExitCodeBadArgument);
    elif s0LowerName in ["insecure", "non-secure"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bzSecureConnections = not fbParseBooleanArgument(s0Value);
    elif s0LowerName in ["sv", "segmented-video"]:
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
      bClientShouldProcessSegmentedVideo = True;
      bClientShouldDownloadToFile = True;
      # If a path is provided for downloading, set it. If not, make sure we download by setting it to None
      if s0Value:
        o0ClientShouldDownloadToFileSystemItem = cFileSystemItem(s0Value);
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
    elif s0LowerName in ["show-details"]:
      bzShowDetails = fbParseBooleanArgument(s0Value);
    elif s0LowerName in ["show-body", "show-message-body"]:
      bzShowMessageBody = fbParseBooleanArgument(s0Value);
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
      asRunAsClientArguments.append(sArgument); # This argument only makes sense for clients.
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
  bShowDetails = bzShowDetails if fbIsProvided(bzShowDetails) else False;

  if sRunAs == "client":
    fRunAsClient(
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
      asbRemoveHeadersForLowerNames = asbClientShouldRemoveHeadersForLowerNames,
      dtsbReplaceHeaderNameAndValue_by_sLowerName = dtsbClientShouldReplaceHeaderNameAndValue_by_sLowerName,
      atsbAddHeadersNameAndValue = atsbClientShouldAddHeadersNameAndValue,
      dsbSpoofedHost_by_sbHost = dsbSpoofedHost_by_sbHost,
      n0zTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
      o0CookieStoreJSONFileSystemItem = o0ClientShouldUseCookieStoreJSONFileSystemItem,
      o0DownloadToFileSystemItem = o0ClientShouldDownloadToFileSystemItem,
      o0HTTPRequestFileSystemItem = o0InputFileSystemItem,
      o0HTTPProxyServerURL = o0ClientShouldUseHTTPProxyServerURL,
      o0NetscapeCookiesFileSystemItem = o0ClientShouldUseNetscapeCookiesFileSystemItem,
      o0SaveHTTPResponsesToFileSystemItem = o0SaveHTTPResponsesToFileSystemItem,
      o0URL = o0ClientShouldUseURL,
      s0SetHTTPRequestData = s0ClientShouldSetHTTPRequestData,
      sb0SetHTTPRequestBody = sb0ClientShouldSetHTTPRequestBody,
      sbzSetHTTPVersion = sbzSetHTTPVersion,
      sbzSetMethod = sbzClientShouldSetMethod,
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