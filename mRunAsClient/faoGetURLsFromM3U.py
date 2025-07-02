from mHTTPProtocol import cInvalidURLException;

gbDebugOutput = False;

def faoGetURLsFromM3U(sM3UContents, oBaseURL):
  # This is as tolerant and simple as possible:
  # - ignores all lines starting with "#" that are not known to be relevant.
  #   - does not check for Extended M3U "#M3UEXT" header
  #   - ignores Extended M3U "#M3UENC:" header
  # - ignores all lines that do not contain a valid URL.
  aoURLs = [];
  for sLine in sM3UContents.split("\n"):
    sLine = sLine.rstrip("\r").strip();
    if not sLine: continue;
    if sLine.startswith("#EXT-X-MAP:URI="):
      # Found to be required, appears to contain header for video files.
      sURL = sLine[len("#EXT-X-MAP:URI="):];
      # May be surrounded by quotes (I do not know if this is required).
      if sURL[0] in "'\"" and sURL[0] == sURL[-1]:
        sURL = sURL[1:-1];
    elif sLine[0] != "#":
      # URLs are always ASCII, so encode whatever Unicode there may be in the URL as UTF-8:
      sURL = sLine;
    else:
      if gbDebugOutput: print("- Comment:    %s" % repr(sLine));
      continue;
    sbURL = bytes(sURL, "utf-8", "strict");
    try:
      oURL = oBaseURL.foFromAbsoluteOrRelativeBytesString(sbURL);
    except cInvalidURLException:
      if gbDebugOutput: print("- Invalid URL: %s" % repr(sbURL));
    else:
      if gbDebugOutput: print("+ Valid URL:   %s" % repr(sbURL));
      aoURLs.append(oURL);
  return aoURLs;
