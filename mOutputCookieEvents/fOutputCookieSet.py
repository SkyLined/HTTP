from mDateTime import cDateTime;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import (
  COLOR_ADD, CHAR_ADD,
  COLOR_INFO,
  COLOR_LIST, CHAR_LIST,
  COLOR_MODIFY, CHAR_MODIFY,
  COLOR_NORMAL,
  COLOR_REMOVE, CHAR_REMOVE,
);
from mCP437 import fsCP437FromBytesString;
oConsole = foConsoleLoader();

def fOutputCookieSet(oCookieStore_unused, oCookie, o0PreviousCookie):
  bCookieExpired = oCookie.fbIsExpired();
  if not bCookieExpired and oCookie.o0ExpirationDateTime is not None:
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
      COLOR_REMOVE, CHAR_REMOVE,
    ] if bCookieExpired else [
      COLOR_ADD, CHAR_ADD,
    ] if bCookieIsNew else [
      COLOR_MODIFY, CHAR_MODIFY,
    ] if bCookieValueWasModified else [
      COLOR_LIST, CHAR_LIST,
    ],
    COLOR_NORMAL, (
      " Session cookie " if oCookie.o0ExpirationDateTime is None else
      " Cookie "
    ), (
      "expired" if bCookieExpired else
      "added" if bCookieIsNew else
      "updated" if bCookieValueWasModified else
      "repeated"
    ), ": ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbName),
    COLOR_NORMAL, " = ",
    [
      COLOR_INFO, fsCP437FromBytesString(oCookie.sbValue),
    ] if len(oCookie.sbValue) < 30 else [
      COLOR_INFO, fsCP437FromBytesString(oCookie.sbValue[:30]),
      COLOR_NORMAL, "...(",
      COLOR_INFO, str(len(oCookie.sbValue)),
      COLOR_NORMAL, " bytes)"
    ],
    COLOR_NORMAL, " (Domain = ",
    COLOR_INFO, fsCP437FromBytesString(oCookie.sbDomainName),
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
