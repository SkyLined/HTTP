from mColorsAndChars import (
  COLOR_INFO,
  COLOR_NORMAL,
);
from mCP437 import fsCP437FromBytesString;

def fasOutputAddress(*, sHost = None, sbHost = None, sIPAddress = None, sbIPAddress = None, uPortNumber = None):
  sHost = sHost or fsCP437FromBytesString(sbHost);
  s0IPAddress = sIPAddress or (fsCP437FromBytesString(sbIPAddress) if sbIPAddress else None);
  return (
    [
      COLOR_INFO,       ("[%s]" if ":" in sHost else "%s") % sHost,
    ]
  ) + (
    [
      COLOR_NORMAL,     ":",
      COLOR_INFO,       str(uPortNumber),
    ] if uPortNumber else []
  ) + (
    [
      COLOR_NORMAL,     " using IP address ",
      COLOR_INFO,       ("[%s]" if ":" in s0IPAddress else "%s") % s0IPAddress,
    ] if s0IPAddress and sHost.lower() != s0IPAddress.lower() else []
  );