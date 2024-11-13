from ..fOutputResponseSent import fOutputResponseSent;

def fOutputFromProxyToClientResponseSent(oConnection, oResponse):
  fOutputResponseSent("P", "C", "client", oConnection, oResponse);
