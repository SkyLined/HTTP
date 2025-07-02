from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();

def ftxHandleRequest_PROPFIND(oServer, oRequest, oBaseFolder):
  oResponse = oRequest.foCreateResponse(
    uzStatusCode = 403, # Forbidden
    bAddContentLengthHeader = True,
  );
  oResponse.oHeaders.foAddHeaderForNameAndValue(b"WWW-Authenticate", b"NTLM");
  return (
    oResponse,
    None, # No next connection handler
  );
