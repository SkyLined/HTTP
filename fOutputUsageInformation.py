from mColorsAndChars import *;
from foConsoleLoader import foConsoleLoader;
from fOutputLogo import fOutputLogo;
oConsole = foConsoleLoader();

def fOutputUsageInformation(bOutputAllOptions = True):
  fOutputLogo();
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
    if not bOutputAllOptions:
        oConsole.fOutput("For a list of all options, run ", COLOR_INFO, "HTTP --help", COLOR_NORMAL, ".");  
        return;
    oConsole.fOutput(COLOR_HILITE, "OPTIONS", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "--arguments", COLOR_NORMAL, "=<", COLOR_INFO, "file path", COLOR_NORMAL, ">");
    oConsole.fOutput("    Load additional arguments from the provided value and insert them in place");
    oConsole.fOutput("    of this argument.");
    
    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Login", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-bl", COLOR_NORMAL, ",  ", COLOR_INFO, "--basic-login=username:password");
    oConsole.fOutput("    Add an `Authorization: basic ...` header with the base64 encoded username and password.");
    
    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Cookies", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-c=<file path>", COLOR_NORMAL, ",  ", COLOR_INFO, "--cookies=<file path>");
    oConsole.fOutput("    Read cookies from a 'Netscape' formatted file for use in requests.");
    oConsole.fOutput("  ", COLOR_INFO, "-s[=<file path>]", COLOR_NORMAL, ",  ", COLOR_INFO, "--cookie-store[=<file path>]");
    oConsole.fOutput("    Read cookies from the given JSON file for use in requests. Any new cookies");
    oConsole.fOutput("    provided by servers are saved to this file. Expired cookies are deleted.");
    oConsole.fOutput("    If no file is provided, a file named 'HTTPCookieStore.json' in the current");
    oConsole.fOutput("    folder is used. If the file does not exist, it will be created.");
    
    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Request options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "--data=<text>");
    oConsole.fOutput("    Send utf-8 encoded \"<text>\" as data in the body of the request.");
    oConsole.fOutput("  ", COLOR_INFO, "-bf=<file path>", COLOR_NORMAL, ",  ", COLOR_INFO, "--body-file=<file path>");
    oConsole.fOutput("    Send the content of the given file in the body of the request.");
    oConsole.fOutput("  ", COLOR_INFO, "-df=<file path>", COLOR_NORMAL, ",  ", COLOR_INFO, "--data-file=<file path>");
    oConsole.fOutput("    Send the utf-8 encoded content of the given file as data in the body of the request.");
    oConsole.fOutput("  ", COLOR_INFO, "--header=<name[:value]>");
    oConsole.fOutput("    Add the given HTTP header to the requests. If no value is provided, the");
    oConsole.fOutput("    header is removed instead. HTTP normally uses a set of default headers");
    oConsole.fOutput("    for each request. This argument can be used to modify them.");
    oConsole.fOutput("  ", COLOR_INFO, "--form=<name[=value]>");
    oConsole.fOutput("    POST the given name-value pair as a `application/x-www-form-urlencoded` form. Use multiple");
    oConsole.fOutput("    arguments to add multiple name-value pairs. A `Content-Type` header will automatically be");
    oConsole.fOutput("    added and the default HTTP method will be POST.");
    

    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Response options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-db", COLOR_NORMAL, ",  ", COLOR_INFO, "--decode", COLOR_NORMAL, ",  ", COLOR_INFO, "--decode-body");
    oConsole.fOutput("    Decode the response body.");
    oConsole.fOutput("  ", COLOR_INFO, "-fdb", COLOR_NORMAL, ",  ", COLOR_INFO, "--fix-decode", COLOR_NORMAL, ",  ", COLOR_INFO, "--fix-decode-body");
    oConsole.fOutput("    Attempt to decode the response body even if the encoding details provided");
    oConsole.fOutput("    by the server are incorrect. This will exhaustively try to decode the body");
    oConsole.fOutput("    using all known encoding types rather than those suggested by the server.");
    oConsole.fOutput("  ", COLOR_INFO, "-dl[=<file path>]", COLOR_NORMAL, ",  ", COLOR_INFO, "--download[=<file path>]");
    oConsole.fOutput("    Download; write the decoded response body to the given file. if no file is");
    oConsole.fOutput("    provided, it is written in the current folder in a file with a name based");
    oConsole.fOutput("    on the request URL.");
    oConsole.fOutput("  ", COLOR_INFO, "-save[=<path>]");
    oConsole.fOutput("    Save the entire response in the file specified by \"<path>\". If no path");
    oConsole.fOutput("    is provided, it is saved in the current folder in a file named based on");
    oConsole.fOutput("    the request URL.");
    
    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Multiple request options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-r", COLOR_NORMAL, ", ", COLOR_INFO, "--max-redirects=<integer>", COLOR_NORMAL, ", ", COLOR_INFO, "--follow-redirects=<integer>");
    oConsole.fOutput("    If the server response with a HTTP 3xx redirect, follow the redirect");
    oConsole.fOutput("    to make another request up to the specified number of times.");
    oConsole.fOutput("  ", COLOR_INFO, "-m3u");
    oConsole.fOutput("    The URL provided represents a playlist and you want to download all files");
    oConsole.fOutput("    in the playlist individually instead of the playlist itself. See also the");
    oConsole.fOutput("    ", COLOR_INFO, "--segmented-m3u", COLOR_NORMAL, " option.");
    oConsole.fOutput("  ", COLOR_INFO, "-sm3u", COLOR_NORMAL, ", ", COLOR_INFO, "--segmented-m3u");
    oConsole.fOutput("    The URL provided represents a playlist and you want to download all files");
    oConsole.fOutput("    in the playlist into a single file instead of the playlist itself. This is");
    oConsole.fOutput("    useful if the playlist represents a single video that is segmented into");
    oConsole.fOutput("    many smaller videos for streaming.");
    oConsole.fOutput("  ", COLOR_INFO, "-sv[=<path>]", COLOR_NORMAL, ", ", COLOR_INFO, "--segmented-video[=<path>]");
    oConsole.fOutput("    The URL provided represents one of many URLs used for a video that is");
    oConsole.fOutput("    streamed from multiple segments. The names of subsequent segments is");
    oConsole.fOutput("    guessed from the initial URL and all of the segments are downloaded");
    oConsole.fOutput("    into a single video file.");

    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Connection options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-s", COLOR_NORMAL, ", ", COLOR_INFO, "--secure", axBoolean);
    oConsole.fOutput("    Check the certificate for HTTPS connections (default). Set to \"false\"");
    oConsole.fOutput("    to allow invalid, expired and self-signed certificates. This does not");
    oConsole.fOutput("    check if all intermediate certificates are provided by the server.");
    oConsole.fOutput("  ", COLOR_INFO, "--very-secure", axBoolean);
    oConsole.fOutput("  ", COLOR_INFO, "--insecure", COLOR_NORMAL, ", ", COLOR_INFO, "--non-secure", axBoolean);
    oConsole.fOutput("    Do not check any certificates for HTTPS connections. Equivalent to ", COLOR_INFO, "--secure=false");
    oConsole.fOutput("  ", COLOR_INFO, "-p[=<URL>]", COLOR_NORMAL, ", ", COLOR_INFO, "--proxy[=<URL>]", COLOR_NORMAL, ", ", COLOR_INFO, "--http-proxy[=<URL>]");
    oConsole.fOutput("    Use the given HTTP proxy to make requests, or automatically determine ");
    oConsole.fOutput("    the proxy if no URL is given.");
    oConsole.fOutput("  ", COLOR_INFO, "-t=<seconds|none>",  COLOR_NORMAL, ", ", COLOR_INFO, "--timeout=<seconds|none>");
    oConsole.fOutput("    Set the response timeout to the given number of seconds. Use 'none' to ");
    oConsole.fOutput("    disable timeouts altogether.");
    oConsole.fOutput("  ", COLOR_INFO, "--spoof:<host>=<spoofed host>");
    oConsole.fOutput("    For URLs that use the first host, all requests will be send to the second");
    oConsole.fOutput("    host instead, without modification. The \"Host\" header, cookies, and HTTPS");
    oConsole.fOutput("    certificate checks are unaffected. This allows you to \"spoof\" the server");
    oConsole.fOutput("    at the first host (DNS name or IP address) using the server at the second.");

    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "Output options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "--show-details", axBoolean);
    oConsole.fOutput("    Show request headers/body and response headers. Set to \"false\" to hide");
    oConsole.fOutput("    them. Does not affect whether the response body is shown or not.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-body", axBoolean);
    oConsole.fOutput("    Show the request/response bodies (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-progress", axBoolean);
    oConsole.fOutput("    Show progress output (default). Set to \"false\" to hide it.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-proxy", axBoolean);
    oConsole.fOutput("    Show progress output (default). Set to \"false\" to hide it.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-request", axBoolean);
    oConsole.fOutput("    Show requests (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", COLOR_INFO, "--show-response", axBoolean);
    oConsole.fOutput("    Show responses (default). Set to \"false\" to hide them.");
    oConsole.fOutput("  ", COLOR_INFO, "--debug", axBoolean);
    oConsole.fOutput("    Show debug output. Set to \"false\" to hide them (default).");
    
    oConsole.fOutput("");
    oConsole.fOutput("  ", COLOR_HILITE, "General options", COLOR_NORMAL, ":");
    oConsole.fOutput("  ", COLOR_INFO, "-h", COLOR_NORMAL, ", ", COLOR_INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", COLOR_INFO, "--license");
    oConsole.fOutput("    Show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--license-update");
    oConsole.fOutput("    Download license updates and show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", COLOR_INFO, "--version-check");
    oConsole.fOutput("    Check for updates and show version information.");
    
    oConsole.fOutput();
    oConsole.fOutput("You can encode characters using \"\\x##\" (e.g. \"\\x41\" == \"A\") in the value of the arguments");
    oConsole.fOutput(COLOR_INFO, "--data", COLOR_NORMAL, ", ",
                     COLOR_INFO, "--data-file", COLOR_NORMAL, ", ",
                     COLOR_INFO, "--header", COLOR_NORMAL, ", and ",
                     COLOR_INFO, "--form", COLOR_NORMAL, ".");
    oConsole.fOutput(COLOR_HILITE, "Exit codes:");
    oConsole.fOutput("  ", COLOR_OK,    "0", COLOR_NORMAL,"  = Success.");
    oConsole.fOutput("  ", COLOR_ERROR, "1", COLOR_NORMAL, "  = There was an internal error: please report the details!");
    oConsole.fOutput("  ", COLOR_ERROR, "2", COLOR_NORMAL, "  = Unable to parse the command-line arguments provided.");
    oConsole.fOutput("  ", COLOR_ERROR, "3", COLOR_NORMAL, "  = There was an error while loading a dependency.");
    oConsole.fOutput("  ", COLOR_ERROR, "4", COLOR_NORMAL, "  = You do not have a valid license to run HTTP.");
    oConsole.fOutput("  ", COLOR_ERROR, "5", COLOR_NORMAL, "  = A file could not be read from.");
    oConsole.fOutput("  ", COLOR_ERROR, "6", COLOR_NORMAL, "  = A file could not be written to.");
    oConsole.fOutput("  ", COLOR_ERROR, "7", COLOR_NORMAL, "  = HTTP was terminated by the user.");
    oConsole.fOutput("  ", COLOR_ERROR, "10", COLOR_NORMAL, "  = The cookies could not be loaded from file.");
    oConsole.fOutput("  ", COLOR_ERROR, "11", COLOR_NORMAL, "  = The cookies could not be saved to file.");
    oConsole.fOutput("  ", COLOR_ERROR, "12", COLOR_NORMAL, "  = The request body could not be read from file.");
    oConsole.fOutput("  ", COLOR_ERROR, "13", COLOR_NORMAL, "  = The response body could not be saved to file.");
    oConsole.fOutput("  ", COLOR_ERROR, "14", COLOR_NORMAL, "  = A secure connection could not be established.");
    oConsole.fOutput("  ", COLOR_ERROR, "15", COLOR_NORMAL, "  = The server did not return a valid response.");
    oConsole.fOutput("  ", COLOR_ERROR, "16", COLOR_NORMAL, " = There were too many consecutive redirects.");
  finally:             
    oConsole.fUnlock();