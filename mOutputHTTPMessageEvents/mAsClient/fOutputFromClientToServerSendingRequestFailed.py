from ..fOutputSendingRequestFailed import fOutputSendingRequestFailed;

def fOutputFromClientToServerSendingRequestFailed(oConnection, oRequest, oException):
  fOutputSendingRequestFailed("C", "S", "server", oConnection, oRequest, oException);