import os, sys;

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
  fOutputToServerFromClientConnectionCreated,
  fOutputToServerFromClientConnectionTerminated,
);
from mOutputHTTPMessageComponents import (
  fOutputHTTPRequest,
  fOutputHTTPResponse,
);
from mOutputHTTPMessageEvents import (
  fOutputToServerFromClientReceivingRequest,
  fOutputToServerFromClientReceivingRequestFailed,
  fOutputToServerFromClientRequestReceived,
  fOutputFromServerToClientSendingResponse,
  fOutputFromServerToClientSendingResponseFailed,
  fOutputFromServerToClientResponseSent,
);
from mOutputSecureConnectionEvents import (
  fOutputToServerFromClientSecuringConnection,
  fOutputToServerFromClientSecuringConnectionFailed,
  fOutputToServerFromClientConnectionSecured,
);
oConsole = foConsoleLoader();

from .ftxHandleRequest import ftxHandleRequest;

def fRunAsServer(
    bDecodeBodyOfHTTPMessages,
    bFailOnDecodeBodyErrors,
    bForceHexOutputOfHTTPMessageBody,
    bSecureConnections,
    bShowProgress,
    bShowRequest,
    bShowResponse,
    bShowDetails,
    n0zTimeoutInSeconds,
    nSendDelayPerByteInSeconds,
    o0BaseFolderFileSystemItem,
    sbzHost,
    uHexOutputCharsPerLine,
    uzPortNumber,
):
  sbHost = sbzHost if fbIsProvided(sbzHost) else cHTTPServer.sbDefaultHost;
  if bSecureConnections:
    assert m0SSL, \
        "mSSL is not available!?";
    sCertificateAuthorityFolderPath = os.path.join(os.getenv("TEMP"), "HTTP.py CA");
    oCertificateAuthority = m0SSL.cCertificateAuthority(sCertificateAuthorityFolderPath, "HTTP.py");
    o0ServerSideSSLContext = oCertificateAuthority.fo0GetServersideSSLContextForHost(sbHost);
    if o0ServerSideSSLContext is None:
      o0ServerSideSSLContext = oCertificateAuthority.foGenerateServersideSSLContextForHost(sbHost);
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
      sbzHost = sbHost,
      uzPortNumber = uzPortNumber,
      o0SSLContext = o0ServerSideSSLContext,
      n0zTransactionTimeoutInSeconds = n0zTimeoutInSeconds,
      n0zIdleTimeoutInSeconds = n0zTimeoutInSeconds,
      nSendDelayPerByteInSeconds = nSendDelayPerByteInSeconds,
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
      COLOR_NORMAL, " to accept connections because the port is already in use.",
    );
    sys.exit(guExitCodeBadArgument);
  except cHTTPServer.cTCPIPPortNotPermittedException:
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " Could not bind to ",
      [
        COLOR_NORMAL, "port ",
        COLOR_INFO, str(uzPortNumber),
      ] if fbIsProvided(uzPortNumber) else [
        COLOR_NORMAL, "the default port",
      ],
      COLOR_NORMAL, " to accept connections because this is not allowed by the Operating System.",
    );
    sys.exit(guExitCodeBadArgument);

  oHTTPServer.fAddCallbacks({
    "received connection from client": fOutputToServerFromClientConnectionCreated,
    "securing connection from client": fOutputToServerFromClientSecuringConnection,
    "securing connection from client failed": fOutputToServerFromClientSecuringConnectionFailed,
    "secured connection from client": fOutputToServerFromClientConnectionSecured,
    "terminated connection from client": fOutputToServerFromClientConnectionTerminated,
    
    "receiving request from client": lambda oHTTPServer, oConnection: (
      bShowProgress and fOutputToServerFromClientReceivingRequest(
        oConnection = oConnection,
      ),
    ),
    "receiving request from client failed": lambda oHTTPServer, oConnection, oException: (
      bShowProgress and fOutputToServerFromClientReceivingRequestFailed(
        oConnection = oConnection,
        oException = oException,
      ),
    ),
    "received request from client": lambda oHTTPServer, oConnection, oRequest: (
      bShowProgress and fOutputToServerFromClientRequestReceived(
        oConnection = oConnection,
        oRequest = oRequest,
      ),
      # We'll show the request now if we don't also show the response
      bShowRequest and not bShowResponse and fOutputHTTPRequest(
        oRequest,
        bShowDetails = bShowDetails,
        bDecodeBody = bDecodeBodyOfHTTPMessages,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
        uHexOutputCharsPerLine = uHexOutputCharsPerLine,
        xPrefix = "",
      ),
    ),
    "sending response to client": lambda oHTTPServer, oConnection, o0Request, oResponse: (
      bShowProgress and fOutputFromServerToClientSendingResponse(
        oConnection = oConnection,
        oResponse = oResponse,
      ),
    ),
    "sending response to client failed": lambda oHTTPServer, oConnection, o0Request, oResponse, oException: (
      bShowProgress and fOutputFromServerToClientSendingResponseFailed(
        oConnection = oConnection,
        oResponse = oResponse,
        oException = oException,
      ),
    ),
    "sent response to client": lambda oHTTPServer, oConnection, o0Request, oResponse: (
      bShowProgress and fOutputFromServerToClientResponseSent(
        oConnection = oConnection,
        oResponse = oResponse,
      ),
      # We'll show the request right before the response if we show both
      bShowRequest and bShowResponse and fOutputHTTPRequest(
        o0Request,
        bShowDetails = bShowDetails,
        bDecodeBody = bDecodeBodyOfHTTPMessages,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
        uHexOutputCharsPerLine = uHexOutputCharsPerLine,
        xPrefix = "",
      ),
      bShowResponse and fOutputHTTPResponse(
        oResponse,
        bShowDetails = bShowDetails,
        bDecodeBody = bDecodeBodyOfHTTPMessages,
        bFailOnDecodeBodyErrors = bFailOnDecodeBodyErrors,
        bForceHexOutputOfBody = bForceHexOutputOfHTTPMessageBody,
        uHexOutputCharsPerLine = uHexOutputCharsPerLine,
        xPrefix = "",
      ),
    ),
  });
  oConsole.fOutput(
    COLOR_NORMAL, "Server URL:  ",
    COLOR_INFO, str(oHTTPServer.foGetURL())
  );
  oConsole.fOutput(
    COLOR_NORMAL, "Root folder: ",
    COLOR_INFO, oBaseFolderFileSystemItem.sPath,
  );
  oHTTPServer.fWait();
