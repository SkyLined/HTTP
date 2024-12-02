from mColorsAndChars import (
  COLOR_INFO,
  COLOR_NORMAL,
);

def faxGetStringOrBytesOutput(sbData, u0MaxLength = None):
  # sbData could be binary data, which we display as HEX bytes
  # or an ASCII string, which we display as is.
  try:
    sData = str(sbData, "ascii", "strict");
  except UnicodeDecodeError:
    sData = " ".join("%02X" % uByte for uByte in sbData);
  if u0MaxLength is not None and len(sData) > u0MaxLength:
    return [
      COLOR_INFO, sData[:u0MaxLength], 
      COLOR_NORMAL, "...(",
      COLOR_INFO, str(len(sData)),
      COLOR_NORMAL, " bytes)",
    ];
  return [ COLOR_INFO, sData ];
