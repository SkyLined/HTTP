import sys;

from mFileSystemItem import cFileSystemItem;
from mHTTPServer import cHTTPServer;
from mNotProvided import fbIsProvided;
try: # mSSL support is optional
  import mSSL as m0SSL;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mSSL'":
    raise;
  m0SSL = None;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ERROR, CHAR_ERROR,
  COLOR_INFO,
  COLOR_NORMAL,
);
from mExitCodes import guExitCodeBadArgument;
from mOutputConnectionEvents import (
  fOutputConnectionFromClientCreated,
  fOutputConnectionFromClientTerminated,
);
from mOutputHTTPMessageComponents import (
  fOutputHTTPRequest,
  fOutputHTTPResponse,
);
from mOutputHTTPMessageEvents import (
  fOutputRequestReceived,
  fOutputResponseSent,
);
oConsole = foConsoleLoader();

from .ftxHandleRequest import ftxHandleRequest;

def fRunAsServer(
    bDecodeBodyOfHTTPMessages,
    bFailOnDecodeBodyErrors,
    bForceHexOutputOfHTTPMessageBody,
    bSecureConnections,
    bzShowDetails,
    bzShowRequest,
    bzShowResponse,
    n0zTimeoutInSeconds,
    o0BaseFolderFileSystemItem,
    sbzHost,
    uHexOutputCharsPerLine,
    uzPortNumber,
):
  bShowRequest = bzShowRequest if fbIsProvided(bzShowRequest) else False;
  bShowResponse = bzShowResponse if fbIsProvided(bzShowResponse) else False;
  bShowDetails = bzShowDetails if fbIsProvided(bzShowDetails) else False;

  if bSecureConnections:
    assert m0SSL, \
        "mSSL is not available!?";
    if not fbIsProvided(sbzHost):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " To create a secure server, you must provide a ",
        COLOR_INFO, "host",
        COLOR_NORMAL, " to use in the certificate.",
      );
      sys.exit(guExitCodeBadArgument);

    sCertificateAuthorityFolderPath = os.path.join(os.getenv("TEMP"), "srv.py CA");
    oCertificateAuthority = m0SSL.cCertificateAuthority(sCertificateAuthorityFolderPath, "srv.py");
    o0ServerSideSSLContext = oCertificateAuthority.fo0GetServersideSSLContextForHost(sbzHost);
    if o0ServerSideSSLContext is None:
      o0ServerSideSSLContext = oCertificateAuthority.foGenerateServersideSSLContextForHost(sbzHost);
  else:
    o0ServerSideSSLContext = None;
  oBaseFolderFileSystemItem = o0BaseFolderFileSystemItem or cFileSystemItem(".");
  try:
    oHTTPServer = cHTTPServer(
      ftxRequestHandler = lambda oHTTPServer, oConnection_unused, oRequest:
        ftxHandleRequest(
          oHTTPServer, 
          oRequest,
          oBaseFolderFileSystemItem,
        ),
      sbzHost = sbzHost,
      uzPortNumber = uzPortNumber,
      o0SSLContext = o0ServerSideSSLContext,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zIdleTimeoutInSeconds = n0zTimeoutInSeconds,
    );
  except cHTTPServer.cTCPIPPortAlreadyInUseAsAcceptorException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Could not bind to ",
        [
          COLOR_NORMAL, "port ",
          COLOR_INFO, str(uzPortNumber),
        ] if fbIsProvided(uzPortNumber) else [
          COLOR_NORMAL, "the default port",
        ],
        COLOR_NORMAL, " to accept connections, as the port is already in use.",
      );
      sys.exit(guExitCodeBadArgument);

  oHTTPServer.fAddCallbacks({
    "connection from client received": fOutputConnectionFromClientCreated,
#    "request error": fOutputRequestFromClientError,
#    "response error": fOutputResponseToClientError,
    "connection from client terminated": fOutputConnectionFromClientTerminated,
  });
  if not bShowRequest:
    # We're not showing the request but we do want to show that we received it:
    oHTTPServer.fAddCallback("request received",
      lambda oHTTPServer, oConnection, oRequest: (
        fOutputRequestReceived(
          oConnection,
          oRequest
        ),
      ),
    );
  if not bShowResponse:
    # We're not showing the response but we do want to show that we sent it:
    oHTTPServer.fAddCallback("response sent",
      lambda oHTTPServer, oConnection, oResponse: (
        fOutputResponseSent(
          oConnection,
          oResponse,
        ),
      ),
    );
  if bShowRequest and not bShowResponse:
    oHTTPServer.fAddCallback("request received",
      lambda oHTTPServer, oConnection, oRequest: (
        fOutputHTTPRequest(
          oRequest,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
    );
  elif bShowResponse:
    oHTTPServer.fAddCallback("request received and response sent",
      lambda oHTTPServer, oConnection, oRequest, oResponse: (
        bShowRequest and fOutputHTTPRequest(
          oRequest,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
        fOutputHTTPResponse(
          oResponse,
          bShowDetails = bShowDetails,
          bDecodeBody = bDecodeBodyOfHTTPMessages,
          bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
          bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
          uHexOutputCharsPerLine = uHexOutputCharsPerLine,
          xPrefix = "",
        ),
      ),
    );
  oConsole.fOutput(
    COLOR_NORMAL, "Server URL:  ",
    COLOR_INFO, str(oHTTPServer.foGetURL())
  );
  oConsole.fOutput(
    COLOR_NORMAL, "Root folder: ",
    COLOR_INFO, oBaseFolderFileSystemItem.sPath,
  );
  oHTTPServer.fWait();
