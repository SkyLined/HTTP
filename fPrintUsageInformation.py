from oConsole import oConsole;
from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fOutput(HILITE,"Usage:");
    oConsole.fOutput(INFO, "  HTTP ", DIM, 
                              "[", INFO, "GET", DIM, "|", INFO, "POST", DIM, "|...] ",
                              "<", INFO, "URL", DIM, "> ",
                              "[", INFO, "HTTP/x.x", DIM, "] ",
                              "[", INFO, "OPTIONS", DIM, "]");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "Options:");
    oConsole.fOutput("  ", INFO, "--help", NORMAL, " or ", INFO, "-h");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", INFO, "--data=<text>");
    oConsole.fOutput("    Send \"<text>\" in the body of the request.");
    oConsole.fOutput("  ", INFO, "--data-file=<path>");
    oConsole.fOutput("    Read the contents of the file specified by \"<path>\" and sent it in the");
    oConsole.fOutput("  body of the request.");
    oConsole.fOutput("  ", INFO, "--download[=<path>]", NORMAL, " or ", INFO, "-dl[=<path>]");
    oConsole.fOutput("    Save the response body in the file specified by \"<path>\". If not path");
    oConsole.fOutput("    is provided, it is save in the current folder in a file named based on");
    oConsole.fOutput("    the request URL.");
    oConsole.fOutput("  ", INFO, "--segmented-video[=<path>]", NORMAL, " or ", INFO, "-sv[=<path>]");
    oConsole.fOutput("    The URL provided represents one of many URLs used for a video that is");
    oConsole.fOutput("    available in multiple segments. HTTP.py will attempt to guess the names");
    oConsole.fOutput("    of subsequent segements and download them all into a single file to.");
    oConsole.fOutput("    combine the segments into a single video file.");
    oConsole.fOutput("  ", INFO, "--follow-redirects", NORMAL, " or ", INFO, "-r");
    oConsole.fOutput("    If the server respondse with a HTTP 3xx redirect, follow the redirect");
    oConsole.fOutput("    and make another request.");
    oConsole.fOutput("  ", INFO, "--decode-body", NORMAL, " or ", INFO, "-db");
    oConsole.fOutput("    Show the decoded body of the response instead of the raw encoded data.");
    oConsole.fOutput("  ", INFO, "--http-proxy=<URL>", NORMAL, " or ", INFO, "-p=<URL>");
    oConsole.fOutput("    Use the given HTTP proxy to make requests.");
    oConsole.fOutput("  ", INFO, "--header=<name:value>");
    oConsole.fOutput("    Add the given HTTP header to the requests.");
    oConsole.fOutput("  ", INFO, "--debug");
    oConsole.fOutput("    Show debug output");
  finally:             
    oConsole.fUnlock();