import re;

from mHTTPProtocol import cURL;

def faoGetURLsFromM3U(sM3UContents):
  # This is as tolerant and simple as possible:
  # - ignores all lines starting with "#"
  #   - does not check for Extended M3U "#M3UEXT" header
  #   - ignores Extended M3U "#M3UENC:" header
  # - ignores all lines that do not contain a valid URL.
  aoURLs = [];
  for sLine in sM3UContents.split("\n"):
    sLine = sLine.rstrip("\r").strip();
    if sLine and sLine[0] != "#":
      # URLs are always ASCII, so encode whatever Unicode there may be in the URL as UTF-8:
      sbPossibleURL = bytes(sLine, "utf-8", "strict");
      try:
        oURL = cURL.foFromBytesString(sbPossibleURL);
      except cURL.cHTTPInvalidURLException:
        pass;
      else:
        aoURLs.append(oURL);
  return aoURLs;
