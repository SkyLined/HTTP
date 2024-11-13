from ..fOutputSendingRequestFailed import fOutputSendingRequestFailed;

def fOutputFromClientToProxySendingRequestFailed(oConnection, oRequest, oProxyServerURL, oException):
  fOutputSendingRequestFailed("C", "P", "proxy", oConnection, oRequest, oException);