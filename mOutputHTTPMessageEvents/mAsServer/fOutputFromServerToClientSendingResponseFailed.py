from ..fOutputRequestReceived import fOutputRequestReceived;
from ..fOutputSendingResponseFailed import fOutputSendingResponseFailed;

def fOutputFromServerToClientSendingResponseFailed(oConnection, oRequest, oResponse, oException):
  fOutputRequestReceived("S", "C", "client", oConnection, oRequest);
  fOutputSendingResponseFailed("S", "C", "client", oConnection, oResponse, oException);
