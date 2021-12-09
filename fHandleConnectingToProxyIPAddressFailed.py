﻿from mConsole import oConsole;

from mColorsAndChars import *;
from mCP437 import fsCP437FromBytesString;
from mNotProvided import *;

def fHandleConnectingToProxyIPAddressFailed(oHTTPClient, oException, oProxyServerURL, sIPAddress, sbzHostname):
  # We only show this message if the user provided a hostname instead of an IP address.
  if fbIsProvided(sbzHostname):
    oConsole.fOutput(
      COLOR_ACTIVE,     "C",
      COLOR_ERROR,      "×",
      COLOR_ERROR,      "P",
      COLOR_NORMAL,     " ",
      COLOR_INACTIVE,   "S",
      COLOR_NORMAL, " Connecting to proxy ",
      COLOR_INFO, str(oProxyServerURL),
      COLOR_NORMAL, " using IP address ",
      COLOR_INFO, sIPAddress,
      COLOR_NORMAL, "!",
    );
    oConsole.fOutput(
      "    ",
      COLOR_INFO, CHAR_INFO, 
      COLOR_NORMAL, " ",
      COLOR_HILITE, str(oException.sMessage),
      COLOR_NORMAL, ".",
    );

