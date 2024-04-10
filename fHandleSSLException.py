from mColorsAndChars import *;
oConsole = foConsoleLoader();

def fHandleSSLException(oHTTPClient, oException):
  if isinstance(oException, oHTTPClient.cSSLSecureTimeoutException):
    sErrorMessage = "Securing the connection to the server timed out";
  elif isinstance(oException, oHTTPClient.cSSLWrapSocketException):
    sErrorMessage = "Securely wrapping the connection to the server failed";
  elif isinstance(oException, oHTTPClient.cSSLUnknownCertificateAuthorityException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a certificate with an unknown certificate authority";
  elif isinstance(oException, oHTTPClient.cSSLIncompleteCertificateChainException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a certificate with an incomplete certificate chain";
  elif isinstance(oException, oHTTPClient.cSSLInvalidCertificateException):
    sErrorMessage = "Securing the connection to the server failed because the server provided an invalid certificate";
  elif isinstance(oException, oHTTPClient.cSSLInvalidCertificateChainException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a certificate with an invalid certificate chain";
  elif isinstance(oException, oHTTPClient.cSSLInvalidCertificateExpiredException):
    sErrorMessage = "Securing the connection to the server failed because the server provided an expired certificate";
  elif isinstance(oException, oHTTPClient.cSSLInvalidCertificateRevocationListException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a certificate with an invalid certificate revocation list";
  elif isinstance(oException, oHTTPClient.cSSLInvalidCertificateRevocationListNotAvailableException):
    sErrorMessage = "Securing the connection to the server failed because the certificate revocation list is not available";
  elif isinstance(oException, oHTTPClient.cSSLInvalidHostForCertificateException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a certificate that does not apply to the host of the server";
  elif isinstance(oException, oHTTPClient.cSSLInvalidSelfSignedCertificateException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a self-signed certificate";
  elif isinstance(oException, oHTTPClient.cSSLInvalidSelfSignedCertificateInChainException):
    sErrorMessage = "Securing the connection to the server failed because the server provided a self-signed certificate in the certificate chain";
  elif isinstance(oException, oHTTPClient.cSSLSecureHandshakeException):
    sErrorMessage = "Securing the connection to the server failed because of an error during the handshake";
  elif isinstance(oException, oHTTPClient.cSSLCannotGetRemoteCertificateException):
    sErrorMessage = "Securing the connection to the server failed because the server certificate cannot be retrieved";
  else:
    sErrorMessage = f"Securing the connection to the server failed: {repr(oException)}";
  oConsole.fOutput(
    "      ",
    COLOR_ERROR, CHAR_ERROR,
    COLOR_NORMAL, " ", sErrorMessage, ".",
  );
  o0SSLContext = oException.dxDetails.get("oSSLContext");
  if o0SSLContext:
    for sLine in o0SSLContext.fasGetDetails():
      oConsole.fOutput(
        "          ", sLine,
      );
  d0xPeerCertificate = oException.dxDetails.get("dxPeerCertificate");
  if d0xPeerCertificate:
    for (sName, xValue) in d0xPeerCertificate.items():
      oConsole.fOutput(
        "          ",
        COLOR_NORMAL, str(sName),
        COLOR_DIM, ": ",
        COLOR_NORMAL, repr(xValue),
      );
