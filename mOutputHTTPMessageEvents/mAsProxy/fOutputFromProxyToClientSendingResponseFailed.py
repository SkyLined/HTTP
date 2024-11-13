from ..fOutputSendingResponseFailed import fOutputSendingResponseFailed;

def fOutputFromProxyToClientSendingResponseFailed(oConnection, oResponse, oException):
  fOutputSendingResponseFailed("P", "C", "client", oConnection, oResponse, oException)