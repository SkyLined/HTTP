from oConsole import oConsole;

from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fOutput(HILITE,"Usage:");
    oConsole.fOutput(INFO, "  HTTP ", DIM, 
                              "[", INFO, "GET", DIM, "|", INFO, "POST", DIM, "|...] ",
                              "<", HILITE, "URL", DIM, "> ",
                              "[", INFO, "HTTP/x.x", DIM, "] ",
                              "[", HILITE, "OPTIONS", DIM, "]");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "OPTIONS", NORMAL, ":");
    oConsole.fOutput("  ", INFO, "-h", NORMAL, ", ", INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", INFO, "-v", NORMAL, ", ", INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", INFO, "-r", NORMAL, ", ", INFO, "--follow-redirects");
    oConsole.fOutput("    If the server respondse with a HTTP 3xx redirect, follow the redirect");
    oConsole.fOutput("    and make another request.");
    oConsole.fOutput("  ", INFO, "-dl[=<path>]", NORMAL, ",  ", INFO, "--download[=<path>]");
    oConsole.fOutput("    Save the response body in the file specified by \"<path>\". If no path");
    oConsole.fOutput("    is provided, it is save in the current folder in a file named based on");
    oConsole.fOutput("    the request URL.");
    oConsole.fOutput("  ", INFO, "-sv[=<path>]", NORMAL, ", ", INFO, "--segmented-video[=<path>]");
    oConsole.fOutput("    The URL provided represents one of many URLs used for a video that is");
    oConsole.fOutput("    available in multiple segments. HTTP.py will attempt to guess the names");
    oConsole.fOutput("    of subsequent segements and download them all into a single file to.");
    oConsole.fOutput("    combine the segments into a single video file.");
    oConsole.fOutput("  ", INFO, "--header=<name[:value]>");
    oConsole.fOutput("    Add the given HTTP header to the requests. If no value is provided, the");
    oConsole.fOutput("    header is removed instead. HTTP normally uses a set of default headers");
    oConsole.fOutput("    for each request. This argument can be used to modify them.");
    oConsole.fOutput("  ", INFO, "--data=<text>");
    oConsole.fOutput("    Send \"<text>\" in the body of the request.");
    oConsole.fOutput("  ", INFO, "--df=<path>", NORMAL, ", ", INFO, "--data-file=<path>");
    oConsole.fOutput("    Read the contents of the file specified by \"<path>\" and sent it in the");
    oConsole.fOutput("    body of the request.");
    oConsole.fOutput("  ", INFO, "-db", NORMAL, ", ", INFO, "--decode-body");
    oConsole.fOutput("    Show the decoded body of the response instead of the raw encoded data.");
    oConsole.fOutput("  ", INFO, "-p[=<URL>", NORMAL, ", ", INFO, "--http-proxy[=<URL>]");
    oConsole.fOutput("    Use the given HTTP proxy to make requests, or automatically determine ");
    oConsole.fOutput("    the proxy if no URL is given.");
    oConsole.fOutput("  ", INFO, "-u", NORMAL, ", ", INFO, "--unsecured");
    oConsole.fOutput("    Ignore all certificate error in HTTPS connections.");
    oConsole.fOutput("  ", INFO, "--no-progress");
    oConsole.fOutput("    Do not show progress output.");
    oConsole.fOutput("  ", INFO, "--no-request");
    oConsole.fOutput("    Do not show requests.");
    oConsole.fOutput("  ", INFO, "--no-response");
    oConsole.fOutput("    Do not show responses.");
    oConsole.fOutput("  ", INFO, "--no-details");
    oConsole.fOutput("    Do not show request headers/body or response headers.");
    oConsole.fOutput("  ", INFO, "--debug");
    oConsole.fOutput("    Show debug output.");
  finally:             
    oConsole.fUnlock();