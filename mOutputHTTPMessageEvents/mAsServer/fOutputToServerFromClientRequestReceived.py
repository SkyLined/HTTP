from ..fOutputRequestReceived import fOutputRequestReceived;

def fOutputToServerFromClientRequestReceived(oConnection, oRequest):
  fOutputRequestReceived("S", "C", "client", oConnection, oRequest);