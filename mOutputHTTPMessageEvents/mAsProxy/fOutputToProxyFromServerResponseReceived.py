from ..fOutputResponseReceived import fOutputResponseReceived;

def fOutputToProxyFromServerResponseReceived(oConnection, oResponse):
  fOutputResponseReceived("P", "S", "server", oConnection, oResponse);
