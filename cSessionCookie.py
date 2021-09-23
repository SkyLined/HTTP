import re;

from mDateTime import cDateTime;
from mNotProvided import *;

from mCP437 import fsCP437FromBytesString;

rDomainFormat = re.compile(
  rb"\A"
  rb"\.?" # a single leading '.' is allowed but ignored.
  rb"(?:[a-z0-9_\-]+\.)*" # optional several sub-domains + '.'
  rb"[a-z0-9_\-]+"      # TLD if sub-domains are provided, or hostname if they are not.
  rb"\Z"
);
rPathFormat = re.compile(
  # I do not know how to handle missing leading slashes, superfluous trailing slashes, "//", "/.", or "/..".
  # I've implemented it to allow missing leading slashes and superfluous trailing slashes, not allow "//", and to
  # tread "/." and "/.." as the names of folders, rather than implement directory traversal.
  rb"\A"
  rb"\/?"               # optionally start with '/'
  rb"(?:[^\/\?#]+\/)*"  # optional { several folder names + '/' }
  rb"(?:[^\/\?#]+\/?)?" # optional { folder name + optional '/' }
  rb"\Z"
);

class cSessionCookie(object):
  def __init__(oSelf, sbName, sbValue, o0ExpirationDateTime = None, sb0Domain = None, sb0Path = None, bSecure = False, bHttpOnly = False, sbSameSite = b"Lax"):
    fAssertTypes({
      "sbName": (sbName, bytes),
      "sbValue": (sbValue, bytes),
      "o0ExpirationDateTime": (o0ExpirationDateTime, cDateTime, None),
      "sb0Domain": (sb0Domain, bytes, None),
      "sb0Path": (sb0Path, bytes, None),
      "bSecure": (bSecure, bool),
      "bHttpOnly": (bHttpOnly, bool),
      "sbSameSite": (sbSameSite, bytes),
    });
    assert sbSameSite in [b"Strict", b"Lax", b"None"], \
      "sbSameSite must be \"Strict\",  \"Lax\", or \"None\", not %s" % repr(sbSameSite);
    assert sb0Domain is None or rDomainFormat.match(sb0Domain), \
      "sb0Domain must be None or a valid domain, not %s" % repr(sb0Domain);
    assert sb0Path is None or rPathFormat.match(sb0Path), \
      "sb0Path must be a None or valid path, not %s" % repr(sb0Path);
    oSelf.sbName = sbName;
    oSelf.sbValue = sbValue;
    oSelf.o0ExpirationDateTime = o0ExpirationDateTime;
    oSelf.sb0Domain = sb0Domain;
    oSelf.sb0Path = sb0Path;
    oSelf.bSecure = bSecure;
    oSelf.bHttpOnly = bHttpOnly;
    oSelf.sbSameSite = sbSameSite;
  
  def fbAppliesToDomain(oSelf, sbDomain):
    if oSelf.sb0Domain is None:
      return True; # Applies to all domains
    sbLowerCookieDomainWithLeadingDot = b".%s" % oSelf.sb0Domain.lstrip(b".").lower();
    sbLowerDomainWithLeadingDot = b".%s" % sbDomain.lower();
    if not sbLowerDomainWithLeadingDot.endswith(sbLowerCookieDomainWithLeadingDot):
      return False;
    return True;
  
  def fbAppliesToPath(oSelf, sbPath):
    # I do not know if this match is case sensitive or not. I've implemented it case insensitive.
    if oSelf.sb0Path is None:
      return True; # Applies to all paths.
    sbLowerCookiePathWithLeadingAndTrailingSlash = b"/%s/" % oSelf.sb0Path.strip(b"/").lower();
    if sbLowerCookiePathWithLeadingAndTrailingSlash == b"//":
      sbLowerCookiePathWithLeadingAndTrailingSlash = b"/";
    sbLowerPathWithLeadingAndTrailingSlash = b"/%s/" % sbPath.strip(b"/").lower();
    if sbLowerPathWithLeadingAndTrailingSlash == b"//":
      sbLowerPathWithLeadingAndTrailingSlash = b"/";
    if not sbLowerPathWithLeadingAndTrailingSlash.startswith(sbLowerCookiePathWithLeadingAndTrailingSlash):
      return False; # different path altogether
    return True;
  
  def fbIsExpired(oSelf):
    return False if oSelf.o0ExpirationDateTime is None else oSelf.o0ExpirationDateTime.fbIsBefore(cDateTime.foNow());
  
  def __str__(oSelf):
    asDetails = [
      fsCP437FromBytesString(b"%s=%s" % (oSelf.sbName, oSelf.sbValue)),
    ];
    if oSelf.o0ExpirationDateTime is not None:
      oValidDuration = cDateTime.foNow().foGetDurationForEndDateTime(oSelf.o0ExpirationDateTime);
      oValidDuration.fNormalize();
      asDetails.append("Expires in %s" % oValidDuration.fsToHumanReadableString(u0MaxNumberOfUnitsInOutput = 2));
    if oSelf.sb0Domain is not None:
      asDetails.append("Domain = %s" % fsCP437FromBytesString(oSelf.sb0Domain));
    if oSelf.sb0Path is not None:
      asDetails.append("Path = %s" % fsCP437FromBytesString(oSelf.sb0Path));
    if oSelf.bSecure:
      asDetails.append("Secure");
    if oSelf.bHttpOnly:
      asDetails.append("HttpOnly");
    if oSelf.sbSameSite != "Lax":
      asDetails.append("SameSite = %s" % fsCP437FromBytesString(oSelf.sbSameSite));
    return "; ".join(asDetails);
