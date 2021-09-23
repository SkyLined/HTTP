import re;

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
    oSelf.daoCookies_by_sbOrigin = {};
  
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
    # User-Agent
    if fbIsProvided(oSelf.sbzUserAgent):
      fApplyHeader(b"User-Agent", oSelf.sbzUserAgent, bReplace = True);
    if oSelf.bAddDoNotTrackHeader:
      fApplyHeader(b"DNT", b"1", bReplace = True);
    # Cookies
    aoCookiesForOrigin = oSelf.daoCookies_by_sbOrigin.get(oURL.sbOrigin, []);
    asbCookies = [];
    for oCookie in aoCookiesForOrigin[:]: # Operate on a copy so we can remove expired cookies.
      if (
        oCookie.o0ExpirationDateTime is not None
        and not oCookie.o0ExpirationDateTime.fbIsAfter(cDateTime.foNow())
      ):
        aoCookiesForOrigin.remove(oCookie);
        if f0CookieExpiredCallback:
          f0CookieExpiredCallback(oURL.sbOrigin, oCookie);
        continue; # Expired
      if not oCookie.fbAppliesToDomain(oURL.sbHostname):
        # oConsole.fOutput("Domain (", fsCP437FromBytesString(oURL.sbHostname), ") mismatch for ", str(oCookie));
        continue; # does not match "Domain"
      if not oCookie.fbAppliesToPath(oURL.sbPath):
        # oConsole.fOutput("Path (", fsCP437FromBytesString(oURL.sbPath), ") mismatch for ", str(oCookie));
        continue; # does not match "Path"
      if (
        oCookie.bSecure
        and not oURL.bSecure
      ):
        # oConsole.fOutput("Secure mismatch for ", str(oCookie));
        continue; # not "Secure"
      asbCookies.append(b"%s=%s" % (oCookie.sbName, oCookie.sbValue));
      # oConsole.fOutput("Added session cookie for ", fsCP437FromBytesString(oURL.sbOrigin), " to request: ", str(oCookie));
    if len(asbCookies) > 0:
      fApplyHeader(b"Cookie", b"; ".join(asbCookies), bReplace = False);
  
  def fUpdateFromResponse(oSelf, oResponse, oURL, f0InvalidCookieAttributeCallback = None, f0AddedCookieCallback = None, f0ExpiredCookieCallback = None):
    # f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbAttributeName, sbAttributeValue, bIsNameKnown);
    # f0AddedCookieCallback(oResponse, oURL, oCookie, bIsNewCookie);
    # f0ExpiredCookieCallback(sbOrigin, oCookie);
    # Get a dictionary of existing cookies or an empty one if none exist yet:
    doCookie_by_sbName_for_Origin = dict(
      (oCookie.sbName, oCookie) for oCookie in oSelf.daoCookies_by_sbOrigin.get(oURL.sbOrigin, [])
    );
    # Update the dictionary with any cookies provided in the response:
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
            oMaxAgeDateTimeDuration = cDateTimeDuration.foFromString("%+ds" % uNumberOfSeconds);
          except:
            # What should we do if the client provides an invalid "Max-Age" value?
            if f0InvalidCookieAttributeCallback:
              f0InvalidCookieAttributeCallback(oResponse, oURL, oHeader, sbCookieName, sbCookieValue, sbName, sbValue, True);
          else:
            # expires header takes precedent.
            if not bExpiresHeaderFound:
              dxCookieAttributeArguments["o0ExpirationDateTime"] = cDateTime.foNow().foGetEndDateTimeForDuration(oMaxAgeDateTimeDuration);
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
      bIsNewCookie = oCookie.sbName not in doCookie_by_sbName_for_Origin;
      bIsExpired = oCookie.fbIsExpired();
      if not bIsExpired:
        doCookie_by_sbName_for_Origin[oCookie.sbName] = oCookie;
        if f0AddedCookieCallback:
          f0AddedCookieCallback(oResponse, oURL, oCookie, bIsNewCookie);
      elif not bIsNewCookie:
        oCookie = doCookie_by_sbName_for_Origin[oCookie.sbName];
        del doCookie_by_sbName_for_Origin[oCookie.sbName];
        if f0ExpiredCookieCallback:
          f0ExpiredCookieCallback(oURL.sbOrigin, oCookie);
      # else: we were asked to set a new cookie that is already expired; ignore it.
    # Save the updated cookies in the session.
    oSelf.daoCookies_by_sbOrigin[oURL.sbOrigin] = [
      oCookie for (sbName, oCookie) in doCookie_by_sbName_for_Origin.items()
    ];