import json;

from mDateTime import cDateTime;
from mFileSystemItem import cFileSystemItem;
from mNotProvided import *;

from cSessionCookie import cSessionCookie;

def fxProcessType(sName, xValue, xAcceptedType):
  if not isinstance(xValue, str if xAcceptedType in (bytes, cDateTime) else xAcceptedType):
    raise ValueError(
      "Invalid JSON data: %s (%s) should be of type %s but it is of type %s." % (
        sName, repr(xValue), str(xAcceptedType.__name__), str(xValue.__class__.__name__),
      ),
    );
  if xAcceptedType is bytes:
    try:
      return bytes(xValue, "ascii", "strict");
    except:
      raise ValueError(
        "Invalid JSON data: %s (%s) should be an ASCII string but it is not." % (
          sName, repr(xValue),
        ),
      );
  if xAcceptedType is cDateTime:
    try:
      return cDateTime.foFromString(xValue);
    except:
      raise ValueError(
        "Invalid JSON data: %s (%s) should be an ASCII string containing a date but it is not." % (
          sName, repr(xValue),
        ),
      );
  return xValue;

def fbApplySessionJSONToSession(
  sbSessionJSON,
  oSession,
  bApplyHTTPVersion = True,
  bApplyMaxRedirects = True,
  bApplyUserAgent = True,
  bApplyDoNotTrackHeader = True,
  f0SetHTTPVersionCallback = None, # (oSession, sbHTTPVersion)
  f0SetMaxRedirectsCallback = None, # (oSession, u0MaxRedirects)
  f0SetUserAgentCallback = None, # (oSession, sbUserAgent)
  f0SetAddDoNotTrackHeaderCallback = None, # (oSession, bAddDoNotTrackHeader)
  f0AddCookieCallback = None, # (oSession, sbOrigin, oCookie)
):
  bJSONHasData = False;
  # Parse JSON
  try:
    dxSessionProperties = json.loads(sbSessionJSON);
  except Exception as oException:
    raise ValueError("Could not decode JSON data.");
  # Process data
  for (sSessionPropertyName, xSessionPropertyValue) in dxSessionProperties.items():
    if sSessionPropertyName == "sHTTPVersion":
      if bApplyUserAgent:
        oSession.sbzHTTPVersion = fxProcessType("sHTTPVersion", xSessionPropertyValue, bytes);
        if f0SetHTTPVersionCallback:
          f0SetHTTPVersionCallback(oSession, oSession.sbzHTTPVersion);
        bJSONHasData = True;
    elif sSessionPropertyName == "u0MaxRedirects":
      if bApplyMaxRedirects:
        if xSessionPropertyValue is None:
          oSession.u0MaxRedirects = None;
        else:
          oSession.u0MaxRedirects = fxProcessType("u0MaxRedirects", xSessionPropertyValue, int);
          if oSession.u0MaxRedirects < 0:
            raise ValueError(
              "Invalid JSON data: u0MaxRedirects (%s) should be a positive integer number or zero." % (
                repr(xValue),
              ),
            );
        if f0SetMaxRedirectsCallback:
         f0SetMaxRedirectsCallback(oSession, oSession.u0MaxRedirects);
        bJSONHasData = True;
    elif sSessionPropertyName == "sUserAgent":
      if bApplyUserAgent:
        oSession.sbzUserAgent = fxProcessType("sUserAgent", xSessionPropertyValue, bytes);
        if f0SetUserAgentCallback:
          f0SetUserAgentCallback(oSession, oSession.sbzUserAgent);
        bJSONHasData = True;
    elif sSessionPropertyName == "bAddDoNotTrackHeader":
      if bApplyDoNotTrackHeader:
        oSession.bAddDoNotTrackHeader = fxProcessType("Session.bAddDoNotTrackHeader", xSessionPropertyValue, bool);
        if f0SetAddDoNotTrackHeaderCallback:
          f0SetAddDoNotTrackHeaderCallback(oSession, oSession.bAddDoNotTrackHeader);
        bJSONHasData = True;
    elif sSessionPropertyName == "ddxCookie_by_sName_by_sOrigin":
      for (sOrigin, dxCookie_by_sName) in fxProcessType("Session.ddxCookie_by_sName_by_sOrigin", xSessionPropertyValue, dict).items():
        sbOrigin = fxProcessType("Session.ddxCookie_by_sName_by_sOrigin[sOrigin = %s]" % repr(sOrigin), sOrigin, bytes);
        sCookiesCheckTypeName = "Session.ddxCookie_by_sName_by_sOrigin[%s]" % json.dumps(sOrigin);
        oSession.daoCookies_by_sbOrigin[sbOrigin] = [];
        for (sCookieName, dxCookieProperties) in fxProcessType(sCookiesCheckTypeName, dxCookie_by_sName, dict).items():
          sbCookieName = fxProcessType("%s[sName = %s]" % (sCookiesCheckTypeName, repr(sCookieName)), sCookieName, bytes);
          sCookieCheckTypeName = "%s[%s]" % (sCookiesCheckTypeName, json.dumps(sCookieName));
          sbzCookieValue = zNotProvided;
          dxCookieAttributeArguments = {};
          for (sCookiePropertyName, xCookiePropertyValue) in fxProcessType(sCookieCheckTypeName, dxCookieProperties, dict).items():
            sCookiePropertyCheckTypeName = "%s.%s" % (sCookieCheckTypeName, sCookiePropertyName);
            if sCookiePropertyName == "sValue":
              sbzCookieValue = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            elif sCookiePropertyName == "sExpirationDateTime":
              dxCookieAttributeArguments["o0ExpirationDateTime"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, cDateTime);
            elif sCookiePropertyName == "sDomain":
              dxCookieAttributeArguments["sb0Domain"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            elif sCookiePropertyName == "sPath":
              dxCookieAttributeArguments["sb0Path"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            elif sCookiePropertyName == "bSecure":
              dxCookieAttributeArguments["bSecure"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bool);
            elif sCookiePropertyName == "bHttpOnly":
              dxCookieAttributeArguments["bHttpOnly"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bool);
            elif sCookiePropertyName == "sSameSite":
              dxCookieAttributeArguments["sbSameSite"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            else:
              raise ValueError(
                "Invalid JSON data: %s (%s) is not expected." % (
                  sCookiePropertyCheckTypeName, repr(xCookiePropertyValue),
                ),
              );
          if not fbIsProvided(sbzCookieValue):
            raise ValueError(
              "Invalid JSON data: Cookie %s properties (%s) is missing a \"sValue\" property." % (
                sCookieCheckTypeName, repr(dxCookieProperties),
              ),
            );
          oCookie = cSessionCookie(sbCookieName, sbzCookieValue, **dxCookieAttributeArguments);
          oSession.daoCookies_by_sbOrigin[sbOrigin].append(oCookie);
          if f0AddCookieCallback:
            f0AddCookieCallback(oSession, sbOrigin, oCookie);
          bJSONHasData = True;
  return bJSONHasData;
