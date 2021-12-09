from mConsole import oConsole;
from mDateTime import cDateTime;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputSessionSetCookie(sbOrigin, oCookie, o0PreviousCookie):
  asAttributes = [];
  if oCookie.o0ExpirationDateTime is not None:
    oValidDuration = cDateTime.foNow().foGetDurationForEndDateTime(oCookie.o0ExpirationDateTime);
    oValidDuration.fNormalize();
    asAttributes.append("Expires in %s" % oValidDuration.fsToHumanReadableString(u0MaxNumberOfUnitsInOutput = 2));
  if oCookie.sb0Domain is not None:
    asAttributes.append("Domain = %s" % str(oCookie.sb0Domain, "ascii", "strict"));
  if oCookie.sb0Path is not None:
    asAttributes.append("Path = %s" % str(oCookie.sb0Path, "ascii", "strict"));
  if oCookie.bSecure:
    asAttributes.append("Secure");
  if oCookie.bHttpOnly:
    asAttributes.append("HttpOnly");
  if oCookie.sbSameSite != "Lax":
    asAttributes.append("SameSite = %s" % str(oCookie.sbSameSite, "ascii", "strict"));
  bCookieIsNew = o0PreviousCookie is None;
  bCookieValueWasModified = o0PreviousCookie and o0PreviousCookie.sbValue != oCookie.sbValue;
  oConsole.fOutput(
    "      ",
    [
      COLOR_ADD, CHAR_ADD,
    ] if bCookieIsNew else [
      COLOR_MODIFY, CHAR_MODIFY,
    ] if bCookieValueWasModified else [
      CHAR_LIST,
    ],
    COLOR_NORMAL, " Session cookie ", "added" if bCookieIsNew else "updated" if bCookieValueWasModified else "repeated", " for ",
    COLOR_INFO, fsCP437FromBytesString(sbOrigin),
    COLOR_NORMAL, ": ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbName),
    COLOR_NORMAL, " = ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbValue),
    COLOR_NORMAL, 
    [
      " (", ", ".join(asAttributes), ")",
    ] if asAttributes else [],
    ".",
  );
