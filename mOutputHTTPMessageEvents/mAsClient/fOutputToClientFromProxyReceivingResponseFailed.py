from ..fOutputReceivingResponseFailed import fOutputReceivingResponseFailed;

def fOutputToClientFromProxyReceivingResponseFailed(oConnection, oProxyServerURL, oException):
  fOutputReceivingResponseFailed("C", "P", "proxy", oConnection, oException, oException);