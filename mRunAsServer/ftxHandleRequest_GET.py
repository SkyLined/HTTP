import os;
from mHTTPProtocol import fsb0GetMediaTypeForExtension;

from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();

def foCreateResponseForRequestAndFile(oRequest, oFile):
  sbContent = oFile.fsbRead();
  return oRequest.foCreateResponse(
    uzStatusCode = 200,
    sb0Body = sbContent,
    sb0MediaType = (
      (oFile.s0Extension and fsb0GetMediaTypeForExtension(oFile.s0Extension))
      or b"application/octet-stream"
    ),
    bAddContentLengthHeader = True,
  );

def ftxHandleRequest_GET(oHTTPServer, oRequest, oBaseFolder):
  oRequestURL = oHTTPServer.foGetURLForRequest(oRequest);
  sRequestedPath = oRequestURL.sURLDecodedPath.replace(os.altsep, os.sep).lstrip(os.sep);
  if sRequestedPath:
    o0RequestedFileOrFolder = oBaseFolder.fo0GetDescendant(sRequestedPath, bThrowErrors = False);
  else:
    o0RequestedFileOrFolder = oBaseFolder;
  if o0RequestedFileOrFolder and o0RequestedFileOrFolder.fbIsFile():
    oResponse = foCreateResponseForRequestAndFile(oRequest, o0RequestedFileOrFolder);
  elif o0RequestedFileOrFolder and o0RequestedFileOrFolder.fbIsFolder():
    a0oChildren = o0RequestedFileOrFolder.fa0oGetChildren(bThrowErrors = False) or [];
    aoIndexFiles = [
      oFile for oFile in a0oChildren
      if oFile.fbIsFile(bThrowErrors = False) and oFile.sName.lower().startswith("index.")
    ];
    if len(aoIndexFiles) == 1:
      oResponse = foCreateResponseForRequestAndFile(oRequest, aoIndexFiles[0]);
    else:
      # Perhaps show folder listing?
      oResponse = oRequest.foCreateResponse(
        uzStatusCode = 404,
        sb0Body = b"Not found",
        sb0MediaType = b"text/plain",
        bAddContentLengthHeader = True,
      );
  else:
    oResponse = oRequest.foCreateResponse(
      uzStatusCode = 404,
      sb0Body = b"Not found",
      sb0MediaType = b"text/plain",
      bAddContentLengthHeader = True,
    );
  return (
    oResponse,
    None, # No next connection handler
  );
