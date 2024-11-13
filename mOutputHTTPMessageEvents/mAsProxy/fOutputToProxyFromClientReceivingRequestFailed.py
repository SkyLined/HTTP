from ..fOutputReceivingRequestFailed import fOutputReceivingRequestFailed;

def fOutputToProxyFromClientReceivingRequestFailed(oConnection, oException):
  fOutputReceivingRequestFailed("P", "C", "client", oConnection, oException);