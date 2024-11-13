from ..fOutputSendingRequest import fOutputSendingRequest;

def fOutputFromProxyToServerSendingRequest(oConnection, oRequest):
  fOutputSendingRequest("P", "S", "server", oConnection, oRequest);
