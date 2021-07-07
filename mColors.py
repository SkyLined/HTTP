from mConsole import oConsole;

# Colors used in output for various types of information:
NORMAL =                            0xFF07; # Light gray
DIM =                               0xFF08; # Dark gray
INFO =                              0xFF0B; # Bright blue
HILITE =                            0xFF0F; # Bright white
OK =                                0x0F02; # Green
OK_INFO =                           0x0F0A; # Bright Green
ERROR =                             0xFF04; # Red
ERROR_INFO =                        0xFF0C; # Bright red
WARNING =                           0xFF06; # Yellow
WARNING_INFO =                      0xFF0E; # Bright yellow
UNDERLINE =                        0x10000;

BAR =                               0xFF1B; # Light cyan on Dark blue
PROGRESS =                          0xFFB1; # Dark blue on light cyan

oConsole.uDefaultColor = NORMAL;
oConsole.uDefaultBarColor = BAR;
oConsole.uDefaultProgressColor = PROGRESS;

HTTP_REQUEST_RESPONSE_BOX =         0xFF08;
HTTP_REQUEST_RESPONSE_BOX_HEADER =  0xFF80;

HTTP_REQUEST_STATUS_LINE =          0xFF0E;
HTTP_RESPONSE_STATUS_LINE_1xx =     0xFF0F;
HTTP_RESPONSE_STATUS_LINE_2xx =     0xFF0A;
HTTP_RESPONSE_STATUS_LINE_3xx =     0xFF0A;
HTTP_RESPONSE_STATUS_LINE_4xx =     0xFF0C;
HTTP_RESPONSE_STATUS_LINE_5xx =     0xFF0D;
HTTP_RESPONSE_STATUS_LINE_INVALID = 0xFF04;
HTTP_HEADER_NAME =                  0xFF09;
HTTP_HEADER_VALUE =                 0xFF0B;
HTTP_BODY_DECODED =                 0xFF07;
HTTP_BODY =                         0xFF07;
HTTP_CRLF =                         0xFF08;
HTTP_EOF =                          0xFF80;
