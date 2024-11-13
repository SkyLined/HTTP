from ..fOutputSendingResponseFailed import fOutputSendingResponseFailed;

def fOutputFromServerToClientSendingResponseFailed(oConnection, oResponse, oException):
  fOutputSendingResponseFailed("S", "C", "client", oConnection, oResponse, oException)