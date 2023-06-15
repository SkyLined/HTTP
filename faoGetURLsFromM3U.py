from mHTTPProtocol import cURL;

gbDebugOutput = False;

def faoGetURLsFromM3U(sM3UContents, oBaseURL):
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
        oURL = oBaseURL.foFromAbsoluteOrRelativeBytesString(sbPossibleURL);
      except cURL.cHTTPInvalidURLException:
        if gbDebugOutput: print("- Invalid URL: %s" % repr(sbPossibleURL));
      else:
        if gbDebugOutput: print("+ Valid URL:   %s" % repr(sbPossibleURL));
        aoURLs.append(oURL);
    else:
      if gbDebugOutput: print("- Comment:    %s" % repr(sLine));
  return aoURLs;
