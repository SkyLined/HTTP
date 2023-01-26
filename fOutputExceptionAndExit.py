import sys;

from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

def fOutputExceptionAndExit(oException, uExitCode):
  if hasattr(oException, "sMessage"):
    oConsole.fOutput(
      "  ",
      COLOR_INFO, str(oException.sMessage),
    );
  else:
    oConsole.fOutput(
      "  ",
      COLOR_INFO, str(oException),
    );
  sys.exit(uExitCode);
