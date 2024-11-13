from ..fOutputReceivingResponse import fOutputReceivingResponse;

def fOutputToClientFromProxyReceivingResponse(oConnection, oProxyServerURL):
  fOutputReceivingResponse("C", "P", "proxy", oConnection);