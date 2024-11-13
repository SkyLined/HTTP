from ..fOutputSendingRequestFailed import fOutputSendingRequestFailed;

def fOutputFromProxyToServerSendingRequestFailed(oConnection, oRequest, oException):
  fOutputSendingRequestFailed("P", "S", "server", oConnection, oRequest, oException);