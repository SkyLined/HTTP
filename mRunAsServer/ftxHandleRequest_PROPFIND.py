from mHTTPProtocol import cHTTPHeader, cHTTPHeaders;

from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();


def ftxHandleRequest_PROPFIND(oHTTPServer, oRequest, oBaseFolder):
  oResponse = oRequest.foCreateResponse(
    uzStatusCode = 403, # Forbidden
    bAddContentLengthHeader = True,
  );
  oResponse.oHeaders.foAddHeaderForNameAndValue(b"WWW-Authenticate", b"NTLM");
  return (
    oResponse,
    oRequest.bIndicatesConnectionShouldBeClosed,
    None, # No next connection handler
  );
