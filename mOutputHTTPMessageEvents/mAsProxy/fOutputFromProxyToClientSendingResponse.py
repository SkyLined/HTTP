from ..fOutputSendingResponse import fOutputSendingResponse;

def fOutputFromProxyToClientSendingResponse(oConnection, oResponse):
  fOutputSendingResponse("P", "C", "client", oConnection, oResponse);
