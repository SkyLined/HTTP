from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mExitCodes import *;

def fOutputSessionInvalidCookieAttributeAndExit(sbOrigin, sbCookieName, sbCookieValue, sbAttributeName, sbAttributeValue, bIsNameKnown):
  oConsole.fOutput(
    COLOR_WARNING, CHAR_WARNING,
    COLOR_NORMAL, " Server response from ",
    COLOR_INFO, fsCP437FromBytesString(sbOrigin),
    COLOR_NORMAL, " contains an ",
    COLOR_INFO, "invalid" if bIsNameKnown else "unknown",
    COLOR_NORMAL, " cookie attribute ",
    COLOR_INFO if bIsNameKnown else COLOR_WARNING, fsCP437FromBytesString(sbAttributeName),
    COLOR_NORMAL, " = ",
    COLOR_WARNING if bIsNameKnown else COLOR_INFO, fsCP437FromBytesString(sbAttributeValue),
    COLOR_NORMAL, " for cookie ",
    COLOR_INFO, fsCP437FromBytesString(sbCookieName),
    COLOR_NORMAL, " = ",
    COLOR_INFO, fsCP437FromBytesString(sbCookieValue),
    COLOR_NORMAL, ".",
  );
  sys.exit(guExitCodeNoValidResponseReceived);
