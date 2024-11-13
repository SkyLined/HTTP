from ..fOutputReceivingResponseFailed import fOutputReceivingResponseFailed;

def fOutputToProxyFromServerReceivingResponseFailed(oConnection, oException):
  fOutputReceivingResponseFailed("P", "S", "server", oConnection, oException, oException);