from ..fOutputSendingRequest import fOutputSendingRequest;

def fOutputFromClientToProxySendingRequest(oConnection, oRequest, oProxyServerURL):
  fOutputSendingRequest("C", "P", "proxy", oConnection, oRequest)
