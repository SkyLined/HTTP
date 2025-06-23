sSafeCharacters = " !#$'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
def fsbEncodeHTMLEntities(sData):
  return b"".join(
    bytes(ord(sChar)) if sChar in sSafeCharacters else b"&#%d;" % ord(sChar)
    for sChar in sData
  );