from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mExitCodes import *;
oConsole = foConsoleLoader();

def fOutputInvalidCookieAttribute(oCookieStore, oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbAttributeName, sb0AttributeValue, bIsNameKnown):
  oConsole.fOutput(
    "      ",
    COLOR_WARNING, CHAR_WARNING,
    COLOR_NORMAL, " Server response from ",
    COLOR_INFO, fsCP437FromBytesString(oURL.sbAbsolute),
    [
      COLOR_NORMAL, " contains an ",
      COLOR_INFO, "invalid" if bIsNameKnown else "unknown"
    ] if sb0AttributeValue is not None else (
      COLOR_NORMAL, " is missing a ",
    ),
    COLOR_NORMAL, " cookie attribute ",
    COLOR_INFO if bIsNameKnown else COLOR_WARNING, fsCP437FromBytesString(sbAttributeName),
    [
      COLOR_NORMAL, "=",
      COLOR_WARNING if bIsNameKnown else COLOR_INFO, fsCP437FromBytesString(sb0AttributeValue),
    ] if sb0AttributeValue is not None else [],
    COLOR_NORMAL, " for cookie ",
    COLOR_INFO, fsCP437FromBytesString(sbCookieName),
    COLOR_NORMAL, " = ",
    COLOR_INFO, fsCP437FromBytesString(sbCookieValue),
    COLOR_NORMAL, ".",
  );
