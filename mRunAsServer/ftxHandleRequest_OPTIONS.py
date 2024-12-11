from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();

asbHTTPMethods = [
  b"DELETE",
  b"GET",
  b"HEAD",
  b"OPTIONS",
  b"PATCH",
  b"POST",
  b"PUT",
  b"TRACE",
];
asbWebDAVMethods = [
  b"COPY",
  b"LOCK",
  b"MKCOL",
  b"MOVE",
  b"PROPFIND",
  b"PROPPATCH",
  b"UNLOCK",
];

def ftxHandleRequest_OPTIONS(oHTTPServer, oRequest, oBaseFolder):
  # We will allow everything on anything for now.
  asbAllowedMethods = asbHTTPMethods + asbWebDAVMethods;
  oResponse = oRequest.foCreateResponse(uzStatusCode = 204, bAddContentLengthHeader = True);
  oResponse.oHeaders.foAddHeaderForNameAndValue(b"Allow", b", ".join(asbAllowedMethods));

  # Add CORS headers to response if needed:
  bCORSHeadersAdded = False;
  # Respond to "Origin" with "Access-Control-Allow-Origin"
  aoOriginHeaders = oRequest.oHeaders.faoGetHeadersForName(b"Origin");
  if aoOriginHeaders:
    asbAllowOrigins = [
      oOriginHeader.sbValue
      for oOriginHeader in aoOriginHeaders
      if oOriginHeader.sbValue != b"null"
    ];
    oResponse.oHeaders.foAddHeaderForNameAndValue(b"Access-Control-Allow-Origin", b", ".join(asbAllowOrigins));
    bCORSHeadersAdded = True;
  # Respond to "Access-Control-Request-Method" with "Access-Control-Allow-Methods"
  aoCORSMethodHeaders = oRequest.oHeaders.faoGetHeadersForName(b"Access-Control-Request-Method");
  if aoCORSMethodHeaders:
    oResponse.oHeaders.foAddHeaderForNameAndValue(b"Access-Control-Allow-Methods", b", ".join(asbAllowedMethods));
    bCORSHeadersAdded = True;
  # Respond to "Access-Control-Request-Headers" with "Access-Control-Allow-Headers"
  aoCORSHeadersHeaders = oRequest.oHeaders.faoGetHeadersForName(b"Access-Control-Request-Headers");
  if aoCORSHeadersHeaders:
    asbAllowedHeaders = []
    for oCORSHeadersHeader in aoCORSHeadersHeaders:
      asbAllowedHeaders += [
        sbHeaderName.strip()
        for sbHeaderName in oCORSHeadersHeader.sbValue.split(b",")
      ];
    oResponse.oHeaders.foAddHeaderForNameAndValue(b"Access-Control-Allow-Headers", b", ".join(asbAllowedHeaders));
    bCORSHeadersAdded = True;
  # If we added any CORS headers, we should add a "Access-Control-Max-Age" header too.
  if bCORSHeadersAdded:
    oResponse.oHeaders.foAddHeaderForNameAndValue(b"Access-Control-Max-Age", b"86400"); # 1 day, the max allowed by Firefox
  return (
    oResponse,
    None, # No next connection handler
  );
