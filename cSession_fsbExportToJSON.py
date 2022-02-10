import json;

from mFileSystemItem import cFileSystemItem;
from mNotProvided import *;

def cSession_fsbExportToJSON(oSelf):
  # Create Cookies JSON data:
  ddxCookie_by_sName_by_sLowerDomainName = {};
  for (sbLowerDomainName, aoCookies) in oSelf.daoCookies_by_sbLowerDomainName.items():
    sLowerDomainName = str(sbLowerDomainName, "ascii", "strict");
    dxCookie_by_sName_for_sLowerDomainName = ddxCookie_by_sName_by_sLowerDomainName[sLowerDomainName] = {};
    for oCookie in aoCookies:
      sName = str(oCookie.sbName, "ascii", "strict");
      dxCookie = {
        "sValue": str(oCookie.sbValue, "ascii", "strict"),
        "sDomain": str(oCookie.sbDomain, "ascii", "strict"),
      };
      if oCookie.o0ExpirationDateTime is not None:
        dxCookie["sExpirationDateTime"] = oCookie.o0ExpirationDateTime.fsToString();
      if oCookie.sb0Path is not None:
        dxCookie["sPath"] = str(oCookie.sb0Path, "ascii", "strict");
      if oCookie.bSecure:
        dxCookie["bSecure"] = True;
      if oCookie.bHttpOnly:
        dxCookie["bHttpOnly"] = True;
      if oCookie.sbSameSite != b"Lax":
        dxCookie["sSameSite"] = str(oCookie.sbSameSite, "ascii", "strict");
      ddxCookie_by_sName_by_sLowerDomainName[sLowerDomainName][sName] = dxCookie;
  # Create Session JSON data; only add properties that are non-default:
  dxSessionProperties = {};
  if fbIsProvided(oSelf.sbzHTTPVersion):
    dxSessionProperties["sHTTPVersion"] = str(oSelf.sbzHTTPVersion, "ascii", "strict");
  if oSelf.u0MaxRedirects is not None:
    dxSessionProperties["u0MaxRedirects"] = oSelf.u0MaxRedirects;
  if fbIsProvided(oSelf.sbzUserAgent):
    dxSessionProperties["sUserAgent"] = str(oSelf.sbzUserAgent, "ascii", "strict");
  if oSelf.bAddDoNotTrackHeader:
    dxSessionProperties["bAddDoNotTrackHeader"] = bAddDoNotTrackHeader;
  if ddxCookie_by_sName_by_sLowerDomainName:
    dxSessionProperties["ddxCookie_by_sName_by_sLowerDomainName"] = ddxCookie_by_sName_by_sLowerDomainName;
  # Save JSON data to file.
  sbSessionPropertiesJSON = bytes(json.dumps(dxSessionProperties, sort_keys = True, indent = 2), "ascii", "strict");
  return sbSessionPropertiesJSON;
