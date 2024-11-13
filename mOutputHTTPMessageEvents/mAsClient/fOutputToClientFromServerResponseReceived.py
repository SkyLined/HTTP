from ..fOutputResponseReceived import fOutputResponseReceived;

def fOutputToClientFromServerResponseReceived(oConnection, oResponse):
  fOutputResponseReceived("C", "S", "server", oConnection, oResponse);
