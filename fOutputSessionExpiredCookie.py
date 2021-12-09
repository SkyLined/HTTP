from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputSessionExpiredCookie(sbOrigin, oCookie):
  oConsole.fOutput(
    "      ",
    COLOR_REMOVE, CHAR_REMOVE,
    COLOR_NORMAL, " Session cookie expired for ",
    COLOR_INFO, fsCP437FromBytesString(sbOrigin),
    COLOR_NORMAL, ": ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbName),
    COLOR_NORMAL, " = ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbValue),
    COLOR_NORMAL, ".",
  );
