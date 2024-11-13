from ..fOutputRequestSent import fOutputRequestSent;

def fOutputFromClientToProxyRequestSent(oConnection, oRequest, oProxyServerURL):
  fOutputRequestSent("C", "P", "proxy", oConnection, oRequest);