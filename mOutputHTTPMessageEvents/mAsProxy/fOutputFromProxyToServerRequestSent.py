from ..fOutputRequestSent import fOutputRequestSent;

def fOutputFromProxyToServerRequestSent(oConnection, oRequest):
  fOutputRequestSent("P", "S", "server", oConnection, oRequest);