from ..fOutputSendingRequest import fOutputSendingRequest;

def fOutputFromClientToServerSendingRequest(oConnection, oRequest):
  fOutputSendingRequest("C", "S", "server", oConnection, oRequest);
