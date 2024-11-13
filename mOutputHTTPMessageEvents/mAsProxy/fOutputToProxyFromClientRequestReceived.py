from ..fOutputRequestReceived import fOutputRequestReceived;

def fOutputToProxyFromClientRequestReceived(oConnection, oRequest):
  fOutputRequestReceived("P", "C", "client", oConnection, oRequest);