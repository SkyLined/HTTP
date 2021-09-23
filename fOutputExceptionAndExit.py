import sys;

from mConsole import oConsole;

from mColorsAndChars import *;

def fOutputExceptionAndExit(oException, uExitCode):
  if hasattr(oException, "sMessage"):
    oConsole.fOutput(
      "  ",
      COLOR_INFO, str(oException.sMessage),
    );
    for (sName, xValue) in oException.dxDetails.items():
      oConsole.fOutput(
        "  ",
        COLOR_INFO, str(sName),
        COLOR_NORMAL, " = ",
        COLOR_INFO,
        COLOR_NORMAL, repr(xValue),
      );
  else:
    oConsole.fOutput(
      "  ",
      COLOR_INFO, str(oException),
    );
  sys.exit(uExitCode);
