from foConsoleLoader import foConsoleLoader;
from mColorsAndChars import *;
oConsole = foConsoleLoader();

asLogo = [s.rstrip() for s in """
                                                         _   _                  
           ┄┄┄┄┄┄┄┄╒╦╦┄┄╦╦╕┄╒═╦╦═╕┄╒═╦╦═╕┄╒╦╦══╦╗┄┄┄┄┄┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄          
                    ║╠══╣║    ║║     ║║    ║╠══╩╝  □   ╱╱  ╱╱                   
         ┄┄┄┄┄┄┄┄┄┄╘╩╩┄┄╩╩╛┄┄╘╩╩╛┄┄┄╘╩╩╛┄┄╘╩╩╛┄┄┄┄┄□┄┄╱╱┄┄╱╱┄┄┄┄┄┄┄┄            
                                                      ‾   ‾                     """.split("""
""")];
asColors = [s.rstrip() for s in """
                                                         F   F                  
           99999999FFB99FB39FFFBB39FFFBB39FFFFBB39999999F399F399999999          
                    B3BFB3    B3     B3    B33B33  B   F3  B3                   
         9999999999FB399B3399FB33999FB3399FB3399999399B399B399999999            
                                                      3   3                     """.split("""
""")];
def fOutputLogo():
  # We will use the above ASCII and color data to create a list of arguments
  # that can be passed to oConsole.fOutput in order to output the logo in color:
  oConsole.fLock();
  try:
    for uLineIndex in range(len(asLogo)):
      uCurrentColor = COLOR_NORMAL;
      bUnderlined = False;
      asLogoPrintArguments = [""];
      sCharsLine = asLogo[uLineIndex];
      sColorsLine = asColors[uLineIndex];
      uColorIndex = 0;
      for uColumnIndex in range(len(sCharsLine)):
        try:
          sColor = sColorsLine[uColorIndex];
          uColorIndex += 1;
          if sColor == "_":
            bUnderlined = not bUnderlined;
            sColor = sColorsLine[uColorIndex];
            uColorIndex += 1;
          uColor = (sColor != " " and (0x0F00 + int(sColor, 16)) or COLOR_NORMAL) + (bUnderlined and CONSOLE_UNDERLINE or 0);
          if uColor != uCurrentColor:
            asLogoPrintArguments.extend([uColor, ""]);
            uCurrentColor = uColor;
          sChar = sCharsLine[uColumnIndex];
          asLogoPrintArguments[-1] += sChar;
        except IndexError:
          raise IndexError("Line %d has %d chars but %d colors:\r\n%s\r\n%s" % (uLineIndex + 1, len(sCharsLine), len(sColorsLine), sCharsLine, sColorsLine));
      oConsole.fOutput(*asLogoPrintArguments);
  finally:
    oConsole.fUnlock();

if __name__ == "__main__":
  fOutputLogo();