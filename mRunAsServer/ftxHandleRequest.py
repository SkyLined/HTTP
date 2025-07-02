import os;
from mHTTPProtocol import fsb0GetMediaTypeForExtension;

from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();

from .ftxHandleRequest_GET import ftxHandleRequest_GET;
from .ftxHandleRequest_OPTIONS import ftxHandleRequest_OPTIONS;
from .ftxHandleRequest_PROPFIND import ftxHandleRequest_PROPFIND;

dftxHandleRequest_by_sbMethodName = {
  b"GET": ftxHandleRequest_GET,
  b"OPTIONS": ftxHandleRequest_OPTIONS,
  b"PROPFIND": ftxHandleRequest_PROPFIND,
};
  
def ftxHandleRequest(oHTTPServer, oRequest, oBaseFolder):
  f0txHandleRequest = dftxHandleRequest_by_sbMethodName.get(oRequest.sbMethod);
  if f0txHandleRequest:
    return f0txHandleRequest(oHTTPServer, oRequest, oBaseFolder);
  return (
    oRequest.foCreateResponse(uzStatusCode = 405), # Method not allowed.
    None, # No next connection handler
  );
