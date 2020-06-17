from oConsole import oConsole;

# Colors used in output for various types of information:
NORMAL =            0x0F07; # Light gray
DIM =               0x0F08; # Dark gray
INFO =              0x0F0B; # Bright blue
HILITE =            0x0F0F; # Bright white
ERROR =             0x0F04; # Red
ERROR_INFO =        0x0F0C; # Bright red
WARNING =           0x0F06; # Yellow
WARNING_INFO =      0x0F0E; # Bright yellow
UNDERLINE =        0x10000;

oConsole.uDefaultColor = NORMAL;
oConsole.uDefaultBarColor = 0xFF1B; # Light cyan on Dark blue
oConsole.uDefaultProgressColor = 0xFFB1; # Dark blue on light cyan

HTTP_REQUEST_STATUS_LINE = 0x0F0E;
HTTP_STATUS_LINE_1xx =  0x0F0F;
HTTP_STATUS_LINE_2xx =  0x0F0A;
HTTP_STATUS_LINE_3xx =  0x0F0A;
HTTP_STATUS_LINE_4xx =  0x0F0C;
HTTP_STATUS_LINE_5xx =  0x0F0D;
HTTP_STATUS_LINE_INVALID = 0x0F04;
HTTP_HEADER_NAME =      0x0F09;
HTTP_HEADER_VALUE =     0x0F0B;
HTTP_BODY_DECODED =     0x0F07;
HTTP_BODY =             0x0F08;

