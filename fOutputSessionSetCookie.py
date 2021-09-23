from mConsole import oConsole;
from mDateTime import cDateTime;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;

def fOutputSessionSetCookie(sbOrigin, oCookie, bIsAddedCookie, bIsModifiedCookie):
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
  oConsole.fOutput(
    "  ",
    [
      COLOR_ADD, CHAR_ADD,
    ] if bIsAddedCookie else [
      COLOR_MODIFY, CHAR_MODIFY,
    ] if bIsModifiedCookie else [
      CHAR_LIST,
    ],
    COLOR_NORMAL, " Session cookie ", "added " if bIsAddedCookie else "updated " if bIsModifiedCookie else "", "for ",
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
