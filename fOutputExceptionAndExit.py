import sys;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

gbDebugOutput = False;

def fOutputExceptionAndExit(oException, uExitCode):
  if hasattr(oException, "sMessage"):
    oConsole.fOutput(
      COLOR_ERROR, CHAR_ERROR,
      COLOR_NORMAL, " ",
      COLOR_INFO, str(oException.sMessage),
    );
  else:
    oConsole.fOutput(
      "  ",
      COLOR_INFO, str(oException),
    );
  if gbDebugOutput and hasattr(oException, "dxDetails"):
    for (sName, xValue) in oException.dxDetails.items():
      oConsole.fOutput(
        "    ",
        COLOR_NORMAL, str(sName),
        COLOR_DIM, ": ",
        COLOR_NORMAL, repr(xValue),
      );
  sys.exit(uExitCode);
