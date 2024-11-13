from ..fOutputRequestSent import fOutputRequestSent;

def fOutputFromClientToServerRequestSent(oConnection, oRequest):
  fOutputRequestSent("C", "S", "server", oConnection, oRequest);