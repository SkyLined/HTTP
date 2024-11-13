from .fasOutputAddress import fasOutputAddress;

def fasOutputRemoteAddressForConnection(oConnection):
  return fasOutputAddress(sbHost = oConnection.sbRemoteHost, sbIPAddress = oConnection.sbRemoteIPAddress, uPortNumber = oConnection.uRemotePortNumber);