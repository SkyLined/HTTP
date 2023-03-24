from mDateTime import cDateTime;
from mHTTPProtocol import cHTTPHeader;
from mNotProvided import fbIsProvided;

from mCP437 import fsCP437FromBytesString;

bDebugOutput = False;

def cSession_fApplyHeadersToRequestForURL(oSelf, oRequest, oURL, f0CookieExpiredCallback = None, f0HeaderAppliedCallback = None):
  # f0CookieExpiredCallback(sbOrigin, oCookie);
  # f0HeaderAppliedCallback(oRequest, oURL, oHeader, bReplaced);
  def fApplyHeader(sbName, sbValue, bReplace):
    oHeader = cHTTPHeader(sbName, sbValue);
    if bReplace:
      bReplaced = oRequest.oHeaders.fbReplaceHeaders(oHeader);
    else:
      oRequest.oHeaders.fAddHeader(oHeader);
      bReplaced = False;
    if f0HeaderAppliedCallback:
      f0HeaderAppliedCallback(oRequest, oURL, oHeader, bReplaced);
  if bDebugOutput: print(",-- Applying session headers ".ljust(80, "-"));
  # User-Agent
  if fbIsProvided(oSelf.sbzUserAgent):
    fApplyHeader(b"User-Agent", oSelf.sbzUserAgent, bReplace = True);
    if bDebugOutput: print("| User-Agent: %s" % fsCP437FromBytesString(oSelf.sbzUserAgent));
  if oSelf.bAddDoNotTrackHeader:
    fApplyHeader(b"DNT", b"1", bReplace = True);
    if bDebugOutput: print("| DNT: 1");
  # Cookies
  asbCookieHeaderElements = [];
  if oSelf.daoCookies_by_sbLowerDomainName and bDebugOutput: print("|-- Cookies ".ljust(80, "-"));
  for (sbLowerDomainName, aoCookies) in oSelf.daoCookies_by_sbLowerDomainName.items():
    # a cookie for "example.com" applies to "example.com" as well as sub-domains of example.com:
    sbLowerHostnameWithLeadingDot = b".%s" % oURL.sbHostname.lower();              # .sub-domain.example.com
    if not sbLowerHostnameWithLeadingDot.endswith(b".%s" % sbLowerDomainName):
      if bDebugOutput: print("| - URL hostname (%s) does not match cookie domain %s" % (
        fsCP437FromBytesString(oURL.sbHostname), fsCP437FromBytesString(sbLowerDomainName)
      ));
      continue;
    for oCookie in aoCookies[:]: # Operate on a copy so we can remove expired cookies.
      if (
        oCookie.o0ExpirationDateTime is not None
        and not oCookie.o0ExpirationDateTime.fbIsAfter(cDateTime.foNow())
      ):
        if bDebugOutput: print("| - Cookie expired (%s)" % oCookie);
        aoCookies.remove(oCookie);
        if f0CookieExpiredCallback:
          f0CookieExpiredCallback(oURL.sbOrigin, oCookie);
        continue; # Expired
      if not oCookie.fbAppliesToPath(oURL.sbPath):
        if bDebugOutput: print("| - URL Path (%s) mismatch for cookie %s"  % (
          fsCP437FromBytesString(oURL.sbPath), oCookie
        ));
        continue; # does not match "Path"
      if (
        oCookie.bSecure
        and not oURL.bSecure
      ):
        if bDebugOutput: print("| - URL Secure (%s) mismatch for cookie %s" % (
          "yes" if oURL.bSecure else "no", oCookie,
        ));
        continue; # not "Secure"
      if bDebugOutput: print("| + Cookie applied: %s" % oCookie);
      asbCookieHeaderElements.append(b"%s=%s" % (oCookie.sbName, oCookie.sbValue));
  if len(asbCookieHeaderElements) > 0:
    sbCookieHeader = b"; ".join(asbCookieHeaderElements);
    fApplyHeader(b"Cookie", sbCookieHeader, bReplace = False);
    if bDebugOutput: print("| Cookie: %s" % fsCP437FromBytesString(sbCookieHeader));
