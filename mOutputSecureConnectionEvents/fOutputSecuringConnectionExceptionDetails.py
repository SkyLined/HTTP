try: # mSSL support is optional
  from mSSL import (
    cSSLCannotGetRemoteCertificateException,
    cSSLIncompleteCertificateChainException,
    cSSLInvalidCertificateChainException,
    cSSLInvalidCertificateException,
    cSSLInvalidCertificateExpiredException,
    cSSLInvalidCertificateRevocationListException,
    cSSLInvalidCertificateRevocationListNotAvailableException,
    cSSLInvalidHostForCertificateException,
    cSSLInvalidSelfSignedCertificateException,
    cSSLInvalidSelfSignedCertificateInChainException,
    cSSLSecureHandshakeException,
    cSSLSecureTimeoutException,
    cSSLUnknownCertificateAuthorityException,
    cSSLWrapSocketException,
  );
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mSSL'":
    raise;
  def fOutputSecuringConnectionExceptionDetails(sHeader, oException, sRemoteAddress):
    raise NotImplementedError("mSSL is not available");
else:
  from foConsoleLoader import foConsoleLoader;
  from mColorsAndChars import (
    COLOR_INFO,
    CHAR_LIST,
    COLOR_NORMAL,
  );
  oConsole = foConsoleLoader();

  def fOutputSecuringConnectionExceptionDetails(sHeader, oException, sRemoteAddress):
    if isinstance(oException, cSSLSecureTimeoutException):
      asErrorMessage = [
        COLOR_INFO, "Securing the connection",
        COLOR_NORMAL, " with ", sRemoteAddress,
        COLOR_INFO, " timed out",
      ];
    elif isinstance(oException, cSSLWrapSocketException):
      asErrorMessage = [
        COLOR_INFO, "The socket",
        COLOR_NORMAL, " for the connection with ", sRemoteAddress,
        COLOR_INFO, " could not be wrapped",
      ];
    elif isinstance(oException, cSSLUnknownCertificateAuthorityException):
      asErrorMessage = [
        COLOR_INFO, "One of the certificates",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " has an unknown certificate authority",
      ];
    elif isinstance(oException, cSSLIncompleteCertificateChainException):
      asErrorMessage = [
        COLOR_INFO, "The certificates chain",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " is incomplete",
      ];
    elif isinstance(oException, cSSLInvalidCertificateException):
      asErrorMessage = [
        COLOR_INFO, "One of the certificates",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " is invalid",
      ];
    elif isinstance(oException, cSSLInvalidCertificateChainException):
      asErrorMessage = [
        COLOR_INFO, "The certificate chain",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " is invalid",
      ];
    elif isinstance(oException, cSSLInvalidCertificateExpiredException):
      asErrorMessage = [
        COLOR_INFO, "One of the certificates",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " is expired",
      ];
    elif isinstance(oException, cSSLInvalidCertificateRevocationListException):
      asErrorMessage = [
        COLOR_INFO, "The certificate revocation list",
        COLOR_NORMAL, " for one of the certificates provided by ", sRemoteAddress,
        COLOR_INFO, " is invalid",
      ];
    elif isinstance(oException, cSSLInvalidCertificateRevocationListNotAvailableException):
      asErrorMessage = [
        COLOR_INFO, "The certificate revocation list",
        COLOR_NORMAL, " for one of the certificates provided by ", sRemoteAddress,
        COLOR_INFO, " is not available",
      ];
    elif isinstance(oException, cSSLInvalidHostForCertificateException):
      asErrorMessage = [
        COLOR_INFO, "The certificate",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " does not apply to the host name of the server",
      ];
    elif isinstance(oException, cSSLInvalidSelfSignedCertificateException):
      asErrorMessage = [
        COLOR_INFO, "The certificate",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " is self-signed",
      ];
    elif isinstance(oException, cSSLInvalidSelfSignedCertificateInChainException):
      asErrorMessage = [
        COLOR_INFO, "The certificate chain",
        COLOR_NORMAL, " provided by ", sRemoteAddress,
        COLOR_INFO, " contains a self-signed certificate",
      ];
    elif isinstance(oException, cSSLSecureHandshakeException):
      asErrorMessage = [
        COLOR_NORMAL, "There was ",
        COLOR_INFO, "an error during the secure handshake",
        COLOR_NORMAL, " with ", sRemoteAddress,
      ];
    elif isinstance(oException, cSSLCannotGetRemoteCertificateException):
      asErrorMessage = [
        COLOR_INFO, "The certificate",
        COLOR_NORMAL, " for ", sRemoteAddress,
        COLOR_INFO, " could not be retrieved",
      ];
    else:
      asErrorMessage = [
        COLOR_INFO, "There was an unknown error",
        COLOR_NORMAL, " while securing the connection with ", sRemoteAddress,
      ];

    oConsole.fOutput(
      sHeader,
      asErrorMessage,
      COLOR_NORMAL, ".",
    );
    d0xDetails = getattr(oException, "dxDetails", None);
    if d0xDetails:
      a0sCertificateSubjectNames = d0xDetails.get("asCertificateSubjectNames");
      if a0sCertificateSubjectNames:
        oConsole.fOutput(
          "      ",
          "The remote certificate is valid for the following domains:",
        );
        for sCertificateSubjectName in a0sCertificateSubjectNames:
          oConsole.fOutput(
            "      ",
            CHAR_LIST, " ",
            COLOR_INFO, sCertificateSubjectName,
          );
      a0sCertificateIssuerNames =  d0xDetails.get("asCertificateIssuerNames");
      if a0sCertificateIssuerNames:
        oConsole.fOutput(
          "      ",
          "The certificates in the remote certificate chain were issued by the following issuers:",
        );
        for sCertificateIssuerName in a0sCertificateIssuerNames:
          oConsole.fOutput(
            "      ",
            CHAR_LIST, " ",
            COLOR_INFO, sCertificateIssuerName,
          );
