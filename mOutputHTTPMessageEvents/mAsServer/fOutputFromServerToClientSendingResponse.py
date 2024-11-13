from ..fOutputSendingResponse import fOutputSendingResponse;

def fOutputFromServerToClientSendingResponse(oConnection, oResponse):
  fOutputSendingResponse("S", "C", "client", oConnection, oResponse);
