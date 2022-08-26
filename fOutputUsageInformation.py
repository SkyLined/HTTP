from mConsole import oConsole;

from mColorsAndChars import *;

def fOutputUsageInformation():
  oConsole.fLock();
  try:
    axBoolean = ["[=", COLOR_INFO, "true", COLOR_NORMAL, "|", COLOR_INFO, "false", COLOR_NORMAL, "]"];
    oConsole.fOutput(COLOR_HILITE, "Usage:");
    oConsole.fOutput("  ", COLOR_INFO, "HTTP", COLOR_DIM, " ",
                              "[", COLOR_INFO, "GET", COLOR_DIM, "|", COLOR_INFO, "POST", COLOR_DIM, "|...] ",
                              "<", COLOR_HILITE, "URL", COLOR_DIM, "> ",
                              "[", COLOR_INFO, "HTTP/x.x", COLOR_DIM, "] ",
                              "[", COLOR_HILITE, "OPTIONS", COLOR_DIM, "]");
    oConsole.fOutput();
    oConsole.fOutput(COLOR_HILITE, "OPTIONS", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-h", COLOR_NORMAL, ", ", COLOR_INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", COLOR_INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", COLOR_INFO, "--version-check");
    oConsole.fOutput("    Check for updates and show version information.");
    oConsole.fOutput("  ", COLOR_INFO, "--license");
    oConsole.fOutput("    Show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--license-update");
    oConsole.fOutput("    Download license updates and show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--arguments", COLOR_NORMAL, "=<", COLOR_INFO, "file path", COLOR_NORMAL, ">");
    oConsole.fOutput("    Load additional arguments from the provided value and insert them in place");
    oConsole.fOutput("    of this argument.");
    oConsole.fOutput("  ", COLOR_INFO, "-r", COLOR_NORMAL, ", ", COLOR_INFO, "--max-redirects=<integer>");
    oConsole.fOutput("    If the server respondse with a HTTP 3xx redirect, follow the redirect");
    oConsole.fOutput("    to make another request up to the specified number of times.");
    oConsole.fOutput("  ", COLOR_INFO, "-dl[=<path>]", COLOR_NORMAL, ",  ", COLOR_INFO, "--download[=<path>]");
    oConsole.fOutput("    Save the response body in the file specified by \"<path>\". If no path");
    oConsole.fOutput("    is provided, it is save in the current folder in a file named based on");
    oConsole.fOutput("    the request URL.");
    oConsole.fOutput("  ", COLOR_INFO, "-s[=<path>]", COLOR_NORMAL, ",  ", COLOR_INFO, "--session[=<path>]");
    oConsole.fOutput("    Save session properties such as cookies from each response and apply them to each request.");
    oConsole.fOutput("    If \"<path>\" is specified the session properties are loaded from file before the first");
    oConsole.fOutput("    request (if the file exists) and saved to the file after each request.");
    oConsole.fOutput("  ", COLOR_INFO, "-m3u");
    oConsole.fOutput("    The URL provided represents a playlist and you want to download all files in the playlist");
    oConsole.fOutput("    instead of the playlist itself. Can be combined with ", COLOR_INFO, "-sv[=<path>]", COLOR_NORMAL, " to concatinate the files in the playlist in to a single file.");
    oConsole.fOutput("  ", COLOR_INFO, "-sv[=<path>]", COLOR_NORMAL, ", ", COLOR_INFO, "--segmented-video[=<path>]");
    oConsole.fOutput("    The URL provided represents one of many URLs used for a video that is");
    oConsole.fOutput("    available in multiple segments. HTTP.py will attempt to guess the names");
    oConsole.fOutput("    of subsequent segements and download them all into a single file to.");
    oConsole.fOutput("    combine the segments into a single video file.");
    oConsole.fOutput("  ", COLOR_INFO, "--header=<name[:value]>");
    oConsole.fOutput("    Add the given HTTP header to the requests. If no value is provided, the");
    oConsole.fOutput("    header is removed instead. HTTP normally uses a set of default headers");
    oConsole.fOutput("    for each request. This argument can be used to modify them.");
    oConsole.fOutput("  ", COLOR_INFO, "--form=<name[=value]>");
    oConsole.fOutput("    POST the given name-value pair as a `application/x-www-form-urlencoded` form. Use multiple");
    oConsole.fOutput("    arguments to add multiple name-value pairs. A `Content-Type` header will automatically be");
    oConsole.fOutput("    added and the default HTTP method will be POST.");
    oConsole.fOutput("  ", COLOR_INFO, "--basic-login=username:password");
    oConsole.fOutput("    Add an `Authorization: basic ...` header with the base64 encoded username and password.");
    oConsole.fOutput("  ", COLOR_INFO, "--data=<text>");
    oConsole.fOutput("    Send \"<text>\" in the body of the request.");
    oConsole.fOutput("  ", COLOR_INFO, "--df=<path>", COLOR_NORMAL, ", ", COLOR_INFO, "--data-file=<path>");
    oConsole.fOutput("    Read the contents of the file specified by \"<path>\" and sent it in the");
    oConsole.fOutput("    body of the request.");
    oConsole.fOutput("  ", COLOR_INFO, "-db", COLOR_NORMAL, ", ", COLOR_INFO, "--decode-body", COLOR_NORMAL, axBoolean);
    oConsole.fOutput("    Show the decoded body of the response instead of the raw encoded data.");
    oConsole.fOutput("  ", COLOR_INFO, "-p[=<URL>", COLOR_NORMAL, ", ", COLOR_INFO, "--http-proxy[=<URL>]");
    oConsole.fOutput("    Use the given HTTP proxy to make requests, or automatically determine ");
    oConsole.fOutput("    the proxy if no URL is given.");
    oConsole.fOutput("  ", COLOR_INFO, "-s", COLOR_NORMAL, ", ", COLOR_INFO, "--secure", axBoolean);
    oConsole.fOutput("    Check all certificates for HTTPS connections (default). Set to.");
    oConsole.fOutput("    \"false\" to allow invalid, expired and self-signed certificates.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-progress", axBoolean);
    oConsole.fOutput("    Show progress output (default). Set to \"false\" to hide it.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-request", axBoolean);
    oConsole.fOutput("    Show requests (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-response", axBoolean);
    oConsole.fOutput("    Show responses (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-details", axBoolean);
    oConsole.fOutput("    Show request headers/body and response headers. Set to \"false\" to hide");
    oConsole.fOutput("    them. Does not affect whether the response body is shown or not.");
    oConsole.fOutput("  ", COLOR_INFO, "--debug", axBoolean);
    oConsole.fOutput("    Show debug output. Set to \"false\" to hide them (default).");
    oConsole.fOutput();
    oConsole.fOutput("You can encode characters using \"\\x##\" (e.g. \"\\x41\" == \"A\") in the value of the arguments");
    oConsole.fOutput(COLOR_INFO, "--data", COLOR_NORMAL, ", ",
                     COLOR_INFO, "--data-file", COLOR_NORMAL, ", ",
                     COLOR_INFO, "--header", COLOR_NORMAL, ", and ",
                     COLOR_INFO, "--form", COLOR_NORMAL, ".");
    oConsole.fOutput(COLOR_HILITE, "Exit codes:");
    oConsole.fOutput("  ", COLOR_OK,    "0", COLOR_NORMAL,"  = Success.");
    oConsole.fOutput("  ", COLOR_ERROR, "1", COLOR_NORMAL, "  = Unable to parse the command-line arguments provided.");
    oConsole.fOutput("  ", COLOR_ERROR, "2", COLOR_NORMAL, "  = There was an internal error: please report the details!");
    oConsole.fOutput("  ", COLOR_ERROR, "3", COLOR_NORMAL, "  = You do not have a valid license to run HTTP.");
    oConsole.fOutput("  ", COLOR_ERROR, "10", COLOR_NORMAL, "  = The session could not be loaded from file.");
    oConsole.fOutput("  ", COLOR_ERROR, "11", COLOR_NORMAL, "  = The session could not be saved to file.");
    oConsole.fOutput("  ", COLOR_ERROR, "12", COLOR_NORMAL, "  = The request body could not be read from file.");
    oConsole.fOutput("  ", COLOR_ERROR, "13", COLOR_NORMAL, "  = The response body could not be saved to file.");
    oConsole.fOutput("  ", COLOR_ERROR, "14", COLOR_NORMAL, "  = A secure connection could not be established.");
    oConsole.fOutput("  ", COLOR_ERROR, "15", COLOR_NORMAL, "  = The server did not return a valid response.");
    oConsole.fOutput("  ", COLOR_ERROR, "16", COLOR_NORMAL, " = There were too many consecutive redirects.");
  finally:             
    oConsole.fUnlock();