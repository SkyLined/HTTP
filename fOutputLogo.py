from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

asLogo = [s.rstrip() for s in """
                   ___  ___ ______ ______ _______     __ __                   |
           ┄╌──────╒╦╦╶╴╦╦╕─╒═╦╦═╕─╒═╦╦═╕─╒╦╦══╦╗╶╴■╶─╱╱─╱╱─────╌┄            |
                 ░▒▓║╠══╣║▓▒▒▓║║▓▒░▒▓║║▓▒▒▓║╠══╩╝▓▒▒▓╱╱▓╱╱▓▒░                |
         ┄╌────────╘╩╩╶╴╩╩╛──╘╩╩╛───╘╩╩╛──╘╩╩╛───╴▀╶╱╱─╱╱─────╌┄              |
                   ‾‾‾  ‾‾‾  ‾‾‾‾   ‾‾‾‾  ‾‾‾‾      ‾‾ ‾‾                    |
                 ∙∙∙ Hacker Tool to Test the Protocol ∙∙∙       """.split("""|
""")];
asFGColors = [s for s in """
                   111  111 111111 111111 1111111     11 11                  |
           99999993FFB93FB33FFFBB33FFFBB33FFFFBB393B93F33F399999999          |
                 111B3BFB31111B311111B31111B33B331111F31B31111               |
         9999999993FB393B3393FB33993FB3393FB33999339B33B399999999            |
                   111  111  1111   1111  1111      11 11                    |
                 87F F77777 F777 77 F777 777 F7777777 F78      """.split("""|
""")];
asBGColors = [s for s in """
                                                                             |
                   111 1111 111111 111111 1111111  1  11 11                  |
                    111111    11     11    111111    11 11                   |
                   111  111  1111   1111  1111    1 11 11                    |
                                                                             |
                                                             """.split("""|
""")];
def fOutputLogo():
  # We will use the above ASCII and color data to create a list of arguments
  # that can be passed to oConsole.fOutput in order to output the logo in color:
  oConsole.fLock();
  try:
    for uLineIndex in range(len(asLogo)):
      uCurrentColor = COLOR_NORMAL;
      asLogoPrintArguments = [""];
      sCharsLine = asLogo[uLineIndex];
      sFGColorsLine = asFGColors[uLineIndex];
      sBGColorsLine = asBGColors[uLineIndex];
      for uColumnIndex in range(len(sCharsLine)):
        try:
          sChar = sCharsLine[uColumnIndex];
          sFGColor = sFGColorsLine[uColumnIndex].strip() or "0";
          sBGColor = sBGColorsLine[uColumnIndex].strip() or "0";
          sColor = sBGColor + sFGColor;
          uColor = (sColor != "00" and (0xFF00 + int(sColor, 16)) or COLOR_NORMAL);
          if uColor != uCurrentColor:
            asLogoPrintArguments.extend([uColor, ""]);
            uCurrentColor = uColor;
          asLogoPrintArguments[-1] += sChar;
        except IndexError:
          raise IndexError("Line %d has %d chars, %d FG colors and %d BG colors:\r\n%s:\r\n%s\r\n%s" % (
            uLineIndex + 1,
            len(sCharsLine),
            len(sFGColorsLine),
            len(sBGColorsLine),
            repr(sCharsLine),
            repr(sFGColorsLine),
            repr(sBGColorsLine),
          ));
      oConsole.fOutput(*asLogoPrintArguments);
  finally:
    oConsole.fUnlock();

if __name__ == "__main__":
  fOutputLogo();