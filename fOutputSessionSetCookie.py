from mDateTime import cDateTime;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputSessionSetCookie(sbOrigin, oCookie, o0PreviousCookie):
  if oCookie.o0ExpirationDateTime is not None:
    oValidDuration = cDateTime.foNow().foGetDurationForEndDateTime(oCookie.o0ExpirationDateTime);
    oValidDuration.fNormalize();
    s0Expires = oValidDuration.fsToHumanReadableString(u0MaxNumberOfUnitsInOutput = 2);
  else:
    s0Expires = None;
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
    COLOR_NORMAL, (
      " Session cookie " if oCookie.o0ExpirationDateTime is None else
      " Cookie "
    ), (
      "added" if bCookieIsNew else
      "updated" if bCookieValueWasModified else
      "repeated"
    ), " for ",
    COLOR_INFO, fsCP437FromBytesString(sbOrigin),
    COLOR_NORMAL, ": ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbName),
    COLOR_NORMAL, " = ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbValue),
    COLOR_NORMAL, " (Domain = ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbDomain),
    [
      COLOR_NORMAL, ", Expires in ",
      COLOR_INFO, s0Expires,
    ] if s0Expires is not None else [],
    [
      COLOR_NORMAL, ", Path = ",
      COLOR_INFO, fsCP437FromBytesString(oCookie.sb0Path),
    ] if oCookie.sb0Path is not None else [],
    [
      COLOR_NORMAL, ", ",
      COLOR_INFO, "Secure",
    ] if oCookie.bSecure else [],
    [
      COLOR_NORMAL, ", ",
      COLOR_INFO, "HttpOnly",
    ] if oCookie.bHttpOnly else [],
    [
      COLOR_NORMAL, ", SameSite = ",
      COLOR_INFO, fsCP437FromBytesString(oCookie.sbSameSite),
    ] if oCookie.sbSameSite != "Lax" else [],
    COLOR_NORMAL, ").",
  );
