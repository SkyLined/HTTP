import re;

gbDebugOutput = False;

from mDateTime import cDateTime;
from mConsole import oConsole;
from mNotProvided import *;
from mHTTPProtocol import cHTTPHeader;

from cSessionCookie import cSessionCookie;
from mCP437 import fsCP437FromBytesString;

asHTTPMonthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
rHTTPDateTimeFormat = re.compile("".join([
  r"\A",
  r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)",       # Day of week name
  r", ",                                  
  r"(\d{2})",                             # Day in month
  r"[ \-]",                               
  r"(%s)" % "|".join(asHTTPMonthNames),   # Month name
  r"[ \-]",                               
  r"(\d{4})",                             # Year
  r" ",                                   
  r"(\d{2})",                             # Hour
  r":",                                   
  r"(\d{2})",                             # Minute
  r":",                                   
  r"(\d{2})",                             # Second
  r" GMT",
  r"\Z",
]));

class cSession(object):
  def __init__(oSelf,
    sbzHTTPVersion = zNotProvided,
    u0MaxRedirects = None,
    sbzUserAgent = zNotProvided,
    bAddDoNotTrackHeader = False,
  ):
    oSelf.sbzHTTPVersion = sbzHTTPVersion;
    oSelf.u0MaxRedirects = u0MaxRedirects;
    oSelf.sbzUserAgent = sbzUserAgent;
    oSelf.bAddDoNotTrackHeader = bAddDoNotTrackHeader;
    oSelf.daoCookies_by_sb0LowerDomainName = {};
  
  def fApplyHeadersToRequestForURL(oSelf, oRequest, oURL, f0CookieExpiredCallback = None, f0HeaderAppliedCallback = None):
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
    if gbDebugOutput: oConsole.fOutput(",-- Applying session headers ", sPadding = "-");
    # User-Agent
    if fbIsProvided(oSelf.sbzUserAgent):
      fApplyHeader(b"User-Agent", oSelf.sbzUserAgent, bReplace = True);
      if gbDebugOutput: oConsole.fOutput("| User-Agent: ", fsCP437FromBytesString(oSelf.sbzUserAgent));
    if oSelf.bAddDoNotTrackHeader:
      fApplyHeader(b"DNT", b"1", bReplace = True);
      if gbDebugOutput: oConsole.fOutput("| DNT: 1");
    # Cookies
    asbCookieHeaderElements = [];
    if oSelf.daoCookies_by_sb0LowerDomainName and gbDebugOutput: oConsole.fOutput("|-- Cookies ", sPadding = "-");
    for (sb0LowerDomainName, aoCookies) in oSelf.daoCookies_by_sb0LowerDomainName.items():
      if sb0LowerDomainName is not None:
        # a cookie for "example.com" applies to "example.com" as well as sub-domains of example.com:
        sbLowerHostnameWithLeadingDot = b".%s" % oURL.sbHostname.lower();              # .sub-domain.example.com
        if not sbLowerHostnameWithLeadingDot.endswith(b".%s" % sb0LowerDomainName):
          if gbDebugOutput: oConsole.fOutput("| - URL hostname (", oURL.sbHostname, ") does not match cookie domain ", fsCP437FromBytesString(sb0LowerDomainName));
          continue;
      for oCookie in aoCookies[:]: # Operate on a copy so we can remove expired cookies.
        if (
          oCookie.o0ExpirationDateTime is not None
          and not oCookie.o0ExpirationDateTime.fbIsAfter(cDateTime.foNow())
        ):
          if gbDebugOutput: oConsole.fOutput("| - Cookie expired (", str(oCookie), ")");
          aoCookies.remove(oCookie);
          if f0CookieExpiredCallback:
            f0CookieExpiredCallback(oURL.sbOrigin, oCookie);
          continue; # Expired
        if not oCookie.fbAppliesToPath(oURL.sbPath):
          if gbDebugOutput: oConsole.fOutput("| - URL Path (", fsCP437FromBytesString(oURL.sbPath), ") mismatch for cookie ", str(oCookie));
          continue; # does not match "Path"
        if (
          oCookie.bSecure
          and not oURL.bSecure
        ):
          if gbDebugOutput: oConsole.fOutput("| - URL Secure (", "yes" if oURL.bSecure else "no", ") mismatch for cookie ", str(oCookie));
          continue; # not "Secure"
        if gbDebugOutput: oConsole.fOutput("| + Cookie applied: ", str(oCookie));
        asbCookieHeaderElements.append(b"%s=%s" % (oCookie.sbName, oCookie.sbValue));
        # oConsole.fOutput("Added session cookie for ", fsCP437FromBytesString(oURL.sbOrigin), " to request: ", str(oCookie));
    if len(asbCookieHeaderElements) > 0:
      sbCookieHeader = b"; ".join(asbCookieHeaderElements);
      fApplyHeader(b"Cookie", sbCookieHeader, bReplace = False);
      if gbDebugOutput: oConsole.fOutput("| Cookie: ", fsCP437FromBytesString(sbCookieHeader));
  
  def fUpdateFromResponse(oSelf, oResponse, oURL, f0InvalidCookieAttributeCallback = None, f0SetCookieCallback = None):
    # f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbAttributeName, sbAttributeValue, bIsNameKnown);
    # f0AddedCookieCallback(oResponse, oURL, oCookie, bIsNewCookie);
    # f0ExpiredCookieCallback(sbOrigin, oCookie);
    # Update the cookies provided in the response:
    for oHeader in oResponse.oHeaders.faoGetHeadersForName(b"Set-Cookie"):
      aCookie_tsbName_and_sbValue = oHeader.fGet_atsbName_and_sbValue();
      # The first name-value pair is the cookie's name and value.
      sbCookieName, sbCookieValue = aCookie_tsbName_and_sbValue.pop(0);
      # Go through any remaining name-value pairs and handle them as cookie attributes. 
      bExpiresHeaderFound = False;
      dxCookieAttributeArguments = {};
      for (sbName, sbValue) in aCookie_tsbName_and_sbValue:
        sbLowerName = sbName.lower();
        if sbLowerName == b"expires":
          # What should we do if the server provides multiple "Expires" values?
          # For now we use the last valid value. TODO: find out if there is a standard.
          sHTTPDateTime = fsCP437FromBytesString(sbValue);
          try:
            (sDay, sMonthName, sYear, sHour, sMinute, sSecond) = rHTTPDateTimeFormat.match(sHTTPDateTime).groups();
          except:
            # What should we do if the server provides an invalid "Expires" value?
            if f0InvalidCookieAttributeCallback:
              f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbName, sbValue, True);
          else:
            uMonth = asHTTPMonthNames.index(sMonthName) + 1;
            oExpiresDateTime = cDateTime.foFromString("%s-%02d-%s %s:%s:%s" % (sYear, uMonth, sDay, sHour, sMinute, sSecond));
            dxCookieAttributeArguments["o0ExpirationDateTime"] = oExpiresDateTime;
            bExpiresHeaderFound = True;
        elif sbLowerName == b"max-age":
          # What should we do if the server provides multiple "Max-Age" values?
          # For now we use the last valid value. TODO: find out if there is a standard.
          try:
            uNumberOfSeconds = int(sbValue);
            if uNumberOfSeconds < 0:
              raise ValueError();
          except ValueError:
            # What should we do if the client provides an invalid "Max-Age" value?
            if f0InvalidCookieAttributeCallback:
              f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbName, sbValue, True);
          else:
            # expires header takes precedent.
            if not bExpiresHeaderFound:
              oMaxAgeDateTimeDuration = cDateTimeDuration.fo0FromString("%+ds" % uNumberOfSeconds);
              oExpirationDateTime = cDateTime.foNow().foGetEndDateTimeForDuration(oMaxAgeDateTimeDuration);
              dxCookieAttributeArguments["o0ExpirationDateTime"] = oExpirationDateTime;
        elif sbLowerName == b"domain":
          # What should we do if the server provides multiple "Domain" values?
          # For now we use the last valid value. TODO: find out if there is a standard.
          dxCookieAttributeArguments["sb0Domain"] = sbValue;
        elif sbLowerName == b"path":
          # What should we do if the server provides multiple "Path" values?
          # For now we use the last valid value. TODO: find out if there is a standard.
          dxCookieAttributeArguments["sb0Path"] = b"/" + sbValue.strip(b"/"); # make sure it starts with a '/' and there is no '/' after the last directory name).
        elif sbLowerName == b"secure":
          # What should we do if the server provides a value for "Secure"?
          # For now we ignore any value. TODO: find out if there is a standard.
          dxCookieAttributeArguments["bSecure"] = True;
        elif sbLowerName == b"httponly":
          # What should we do if the server provides a value for "HttpOnly"?
          # For now we ignore any value. TODO: find out if there is a standard.
          dxCookieAttributeArguments["bHttpOnly"] = True;
        elif sbLowerName == b"samesite":
          # Fix casing if needed.
          sbCapitalizedValue = sbValue[:1].upper() + sbValue[1:].lower();
          if sbCapitalizedValue in (b"Strict", b"Lax", b"None"):
            dxCookieAttributeArguments["sbSameSite"] = sbCapitalizedValue;
          else:
            # What should we do if the client provides an invalid "SameSite" value?
            if f0InvalidCookieAttributeCallback:
              f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbName, sbValue, True);
        else:
          # What should we do if the server provides an unhandled named value?
          if f0InvalidCookieAttributeCallback:
            f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbName, sbValue, False);
      oCookie = cSessionCookie(sbCookieName, sbCookieValue, **dxCookieAttributeArguments);
      aoExistingCookies_for_sb0LowerDomainName = oSelf.daoCookies_by_sb0LowerDomainName.setdefault(oCookie.sb0Domain.lstrip(b"."), []);
      # This can replace or remove an existing cookie with the same name:
      # TODO: should this really be case-sensitive?
      o0PreviousCookie = None;
      for oExistingCookie in aoExistingCookies_for_sb0LowerDomainName:
        if oExistingCookie.sbName == oCookie.sbName:
          aoExistingCookies_for_sb0LowerDomainName.remove(oExistingCookie);
          o0PreviousCookie = oExistingCookie;
      if not oCookie.fbIsExpired():
        aoExistingCookies_for_sb0LowerDomainName.append(oCookie);
      if f0SetCookieCallback:
        f0SetCookieCallback(oResponse, oURL, oCookie, o0PreviousCookie);
