from ..fOutputReceivingResponseFailed import fOutputReceivingResponseFailed;

def fOutputToClientFromServerReceivingResponseFailed(oConnection, oException):
  fOutputReceivingResponseFailed("C", "S", "server", oConnection, oException);