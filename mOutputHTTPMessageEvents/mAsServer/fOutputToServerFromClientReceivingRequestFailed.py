from ..fOutputReceivingRequestFailed import fOutputReceivingRequestFailed;

def fOutputToServerFromClientReceivingRequestFailed(oConnection, oException):
  fOutputReceivingRequestFailed("S", "C", "client", oConnection, oException);