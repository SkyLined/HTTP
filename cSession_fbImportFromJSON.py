import json;

from mDateTime import cDateTime;
from mNotProvided import fbIsProvided, zNotProvided;

from cCookie import cCookie;

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

def cSession_fbImportFromJSON(
  oSelf,
  sbSessionJSON,
  bApplyHTTPVersion = True,
  bApplyMaxRedirects = True,
  bApplyUserAgent = True,
  bApplyDoNotTrackHeader = True,
  f0SetHTTPVersionCallback = None, # (oSession, sbHTTPVersion)
  f0SetMaxRedirectsCallback = None, # (oSession, u0MaxRedirects)
  f0SetUserAgentCallback = None, # (oSession, sbUserAgent)
  f0SetAddDoNotTrackHeaderCallback = None, # (oSession, bAddDoNotTrackHeader)
  f0AddCookieCallback = None, # (oSession, sLowerDomainName, oCookie)
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
        oSelf.sbzHTTPVersion = fxProcessType("sHTTPVersion", xSessionPropertyValue, bytes);
        if f0SetHTTPVersionCallback:
          f0SetHTTPVersionCallback(oSelf, oSelf.sbzHTTPVersion);
        bJSONHasData = True;
    elif sSessionPropertyName == "u0MaxRedirects":
      if bApplyMaxRedirects:
        if xSessionPropertyValue is None:
          oSelf.u0MaxRedirects = None;
        else:
          oSelf.u0MaxRedirects = fxProcessType("u0MaxRedirects", xSessionPropertyValue, int);
          if oSelf.u0MaxRedirects < 0:
            raise ValueError(
              "Invalid JSON data: u0MaxRedirects (%s) should be a positive integer number or zero." % (
                repr(xSessionPropertyValue),
              ),
            );
        if f0SetMaxRedirectsCallback:
         f0SetMaxRedirectsCallback(oSelf, oSelf.u0MaxRedirects);
        bJSONHasData = True;
    elif sSessionPropertyName == "sUserAgent":
      if bApplyUserAgent:
        oSelf.sbzUserAgent = fxProcessType("sUserAgent", xSessionPropertyValue, bytes);
        if f0SetUserAgentCallback:
          f0SetUserAgentCallback(oSelf, oSelf.sbzUserAgent);
        bJSONHasData = True;
    elif sSessionPropertyName == "bAddDoNotTrackHeader":
      if bApplyDoNotTrackHeader:
        oSelf.bAddDoNotTrackHeader = fxProcessType("Session.bAddDoNotTrackHeader", xSessionPropertyValue, bool);
        if f0SetAddDoNotTrackHeaderCallback:
          f0SetAddDoNotTrackHeaderCallback(oSelf, oSelf.bAddDoNotTrackHeader);
        bJSONHasData = True;
    elif sSessionPropertyName == "ddxCookie_by_sName_by_sLowerDomainName":
      ddxCookie_by_sName_by_sLowerDomainName = \
          fxProcessType("Session.ddxCookie_by_sName_by_sLowerDomainName", xSessionPropertyValue, dict);
      for (sLowerDomainName, dxCookie_by_sName) in ddxCookie_by_sName_by_sLowerDomainName.items():
        sbLowerDomainName = fxProcessType("Session.ddxCookie_by_sName_by_sLowerDomainName[sLowerDomainName = %s]" % repr(sLowerDomainName), sLowerDomainName, bytes);
        sCookiesCheckTypeName = "Session.ddxCookie_by_sName_by_sLowerDomainName[%s]" % json.dumps(sLowerDomainName);
        oSelf.daoCookies_by_sbLowerDomainName[sbLowerDomainName] = [];
        for (sCookieName, dxCookieProperties) in fxProcessType(sCookiesCheckTypeName, dxCookie_by_sName, dict).items():
          sbCookieName = fxProcessType("%s[sName = %s]" % (sCookiesCheckTypeName, repr(sCookieName)), sCookieName, bytes);
          sCookieCheckTypeName = "%s[%s]" % (sCookiesCheckTypeName, json.dumps(sCookieName));
          sbzCookieValue = zNotProvided;
          sbzCookieDomain = zNotProvided;
          dxCookieAttributeArguments = {};
          for (sCookiePropertyName, xCookiePropertyValue) in fxProcessType(sCookieCheckTypeName, dxCookieProperties, dict).items():
            sCookiePropertyCheckTypeName = "%s.%s" % (sCookieCheckTypeName, sCookiePropertyName);
            if sCookiePropertyName == "sValue":
              sbzCookieValue = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            elif sCookiePropertyName == "sDomain":
              sbzCookieDomain = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, bytes);
            elif sCookiePropertyName == "sExpirationDateTime":
              dxCookieAttributeArguments["o0ExpirationDateTime"] = fxProcessType(sCookiePropertyCheckTypeName, xCookiePropertyValue, cDateTime);
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
          if not fbIsProvided(sbzCookieDomain):
            raise ValueError(
              "Invalid JSON data: Cookie %s properties (%s) is missing a \"sDomain\" property." % (
                sCookieCheckTypeName, repr(dxCookieProperties),
              ),
            );
          oCookie = cCookie(sbCookieName, sbzCookieValue, sbzCookieDomain, **dxCookieAttributeArguments);
          oSelf.daoCookies_by_sbLowerDomainName[sbLowerDomainName].append(oCookie);
          if f0AddCookieCallback:
            f0AddCookieCallback(oSelf, sbLowerDomainName, oCookie);
          bJSONHasData = True;
  return bJSONHasData;
