from ..fOutputResponseReceived import fOutputResponseReceived;

def fOutputToClientFromProxyResponseReceived(oConnection, oResponse, oProxyServerURL):
  fOutputResponseReceived("C", "P", "proxy", oConnection, oResponse);
