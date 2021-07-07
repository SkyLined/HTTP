from mConsole import oConsole;

from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    axBoolean = ["[=", INFO, "true", NORMAL, "|", INFO, "false", NORMAL, "]"];
    oConsole.fOutput(HILITE,"Usage:");
    oConsole.fOutput("  ", INFO, "HTTP", DIM, " ",
                              "[", INFO, "GET", DIM, "|", INFO, "POST", DIM, "|...] ",
                              "<", HILITE, "URL", DIM, "> ",
                              "[", INFO, "HTTP/x.x", DIM, "] ",
                              "[", HILITE, "OPTIONS", DIM, "]");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "OPTIONS", NORMAL, ":");
    oConsole.fOutput("  ", INFO, "-h", NORMAL, ", ", INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", INFO, "--version-check");
    oConsole.fOutput("    Check for updates and show version information.");
    oConsole.fOutput("  ", INFO, "--license");
    oConsole.fOutput("    Show license information.");
    oConsole.fOutput("  ", INFO, "--license-update");
    oConsole.fOutput("    Download license updates and show license information.");
    oConsole.fOutput("  ", INFO, "--arguments", NORMAL, "=<", INFO, "file path", NORMAL, ">");
    oConsole.fOutput("    Load additional arguments from the provided value and insert them in place");
    oConsole.fOutput("    of this argument.");
    
    oConsole.fOutput("  ", INFO, "-r", NORMAL, ", ", INFO, "--max-redirects=<integer>");
    oConsole.fOutput("    If the server respondse with a HTTP 3xx redirect, follow the redirect");
    oConsole.fOutput("    to make another request up to the specified number of times.");
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
    oConsole.fOutput("  ", INFO, "-db", NORMAL, ", ", INFO, "--decode-body", NORMAL, axBoolean);
    oConsole.fOutput("    Show the decoded body of the response instead of the raw encoded data.");
    oConsole.fOutput("  ", INFO, "-p[=<URL>", NORMAL, ", ", INFO, "--http-proxy[=<URL>]");
    oConsole.fOutput("    Use the given HTTP proxy to make requests, or automatically determine ");
    oConsole.fOutput("    the proxy if no URL is given.");
    oConsole.fOutput("  ", INFO, "-s", NORMAL, ", ", INFO, "--secure", axBoolean);
    oConsole.fOutput("    Check all certificates for HTTPS connections (default). Set to.");
    oConsole.fOutput("    \"false\" to allow invalid, expired and self-signed certificates.");
    oConsole.fOutput("  ", INFO, "--show-progress", axBoolean);
    oConsole.fOutput("    Show progress output (default). Set to \"false\" to hide it.");
    oConsole.fOutput("  ", INFO, "--show-request", axBoolean);
    oConsole.fOutput("    Show requests (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", INFO, "--show-response", axBoolean);
    oConsole.fOutput("    Show responses (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", INFO, "--show-details", axBoolean);
    oConsole.fOutput("    Show request headers/body and response headers. Set to \"false\" to hide");
    oConsole.fOutput("    them. Does not affect whether the response body is shown or not.");
    oConsole.fOutput("  ", INFO, "--debug", axBoolean);
    oConsole.fOutput("    Show debug output. Set to \"false\" to hide them (default).");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "Exit codes:");
    oConsole.fOutput("  ", 0x0F0A, "0", NORMAL," = HTTP did not make any successful requests.");
    oConsole.fOutput("  ", 0x0F0A, "1", NORMAL," = HTTP made at least one successful request (2xx status code).");
    oConsole.fOutput("  ", 0x0F0C, "2", NORMAL, " = HTTP was unable to parse the command-line arguments provided.");
    oConsole.fOutput("  ", 0x0F0C, "3", NORMAL, " = HTTP ran into an internal error: please report the details!");
    oConsole.fOutput("  ", 0x0F0C, "4", NORMAL, " = There was an error while make a request.");
    oConsole.fOutput("  ", 0x0F0C, "5", NORMAL, " = HTTP cannot read from the given source.");
    oConsole.fOutput("  ", 0x0F0C, "6", NORMAL, " = HTTP cannot write to the given destination.");
  finally:             
    oConsole.fUnlock();