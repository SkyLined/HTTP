import json;

from mFileSystemItem import cFileSystemItem;
from mNotProvided import *;

def fsbGetSessionJSONFromSession(oSession):
  # Create Cookies JSON data:
  ddxCookie_by_sName_by_sOrigin = {};
  for (sbOrigin, aoCookies) in oSession.daoCookies_by_sbOrigin.items():
    sOrigin = str(sbOrigin, "ascii", "strict");
    dxCookie_by_sName_for_sOrigin = ddxCookie_by_sName_by_sOrigin[sOrigin] = {};
    for oCookie in aoCookies:
      sName = str(oCookie.sbName, "ascii", "strict");
      dxCookie = {
        "sValue": str(oCookie.sbValue, "ascii", "strict"),
      };
      if oCookie.o0ExpirationDateTime is not None:
        dxCookie["sExpirationDateTime"] = oCookie.o0ExpirationDateTime.fsToString();
      if oCookie.sb0Domain is not None:
        dxCookie["sDomain"] = str(oCookie.sb0Domain, "ascii", "strict");
      if oCookie.sb0Path is not None:
        dxCookie["sPath"] = str(oCookie.sb0Path, "ascii", "strict");
      if oCookie.bSecure:
        dxCookie["bSecure"] = True;
      if oCookie.bHttpOnly:
        dxCookie["bHttpOnly"] = True;
      if oCookie.sbSameSite != b"Lax":
        dxCookie["sSameSite"] = str(oCookie.sbSameSite, "ascii", "strict");
      ddxCookie_by_sName_by_sOrigin[sOrigin][sName] = dxCookie;
  # Create Session JSON data; only add properties that are non-default:
  dxSessionProperties = {};
  if fbIsProvided(oSession.sbzHTTPVersion):
    dxSessionProperties["sHTTPVersion"] = str(oSession.sbzHTTPVersion, "ascii", "strict");
  if oSession.u0MaxRedirects is not None:
    dxSessionProperties["u0MaxRedirects"] = oSession.u0MaxRedirects;
  if fbIsProvided(oSession.sbzUserAgent):
    dxSessionProperties["sUserAgent"] = str(oSession.sbzUserAgent, "ascii", "strict");
  if oSession.bAddDoNotTrackHeader:
    dxSessionProperties["bAddDoNotTrackHeader"] = bAddDoNotTrackHeader;
  if ddxCookie_by_sName_by_sOrigin:
    dxSessionProperties["ddxCookie_by_sName_by_sOrigin"] = ddxCookie_by_sName_by_sOrigin;
  # Save JSON data to file.
  sbSessionPropertiesJSON = bytes(json.dumps(dxSessionProperties, sort_keys = True, indent = 2), "ascii", "strict");
  return sbSessionPropertiesJSON;
