from ..fOutputResponseSent import fOutputResponseSent;

def fOutputFromServerToClientResponseSent(oConnection, oResponse):
  fOutputResponseSent("S", "C", "client", oConnection, oResponse);
