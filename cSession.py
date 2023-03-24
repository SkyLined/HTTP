from mNotProvided import zNotProvided;

from cSession_fApplyHeadersToRequestForURL import cSession_fApplyHeadersToRequestForURL;
from cSession_fbImportFromJSON import cSession_fbImportFromJSON;
from cSession_fsbExportToJSON import cSession_fsbExportToJSON;
from cSession_fUpdateFromResponse import cSession_fUpdateFromResponse;

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
    oSelf.daoCookies_by_sbLowerDomainName = {};
  
  fApplyHeadersToRequestForURL = cSession_fApplyHeadersToRequestForURL;
  fbImportFromJSON = cSession_fbImportFromJSON;
  fsbExportToJSON = cSession_fsbExportToJSON;
  fUpdateFromResponse = cSession_fUpdateFromResponse;
