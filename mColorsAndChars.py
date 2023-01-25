# COMMONLY USED COLOR NAMES
COLOR_DIM                               = 0x0F08; # Dark gray
COLOR_NORMAL                            = 0x0F07; # Light gray
COLOR_HILITE                            = 0x0F0F; # White

COLOR_INFO                              = 0xFF09; # Bright blue
COLOR_LIST                              = 0xFF09; # Bright blue

COLOR_BUSY                              = 0x0F03; # Cyan
COLOR_OK                                = 0x0F02; # Green
COLOR_WARNING                           = 0x0F06; # Brown
COLOR_ERROR                             = 0x0F04; # Red

COLOR_SELECT_YES                        = 0xFF09; # Bright blue
COLOR_SELECT_MAYBE                      = 0xFF09; # Bright blue
COLOR_SELECT_NO                         = 0xFF09; # Bright blue

COLOR_INPUT                             = 0x0F0B; #
COLOR_OUTPUT                            = 0x0F07; #

COLOR_ADD                               = 0x0F0A; # Bright green
COLOR_MODIFY                            = 0x0F0B; # Bright cyan
COLOR_REMOVE                            = 0x0F0C; # Bright red

COLOR_PROGRESS_BAR                      = 0xFF98; # Bright blue on dark gray
COLOR_PROGRESS_BAR_HILITE               = 0xFF91; # Dark blue on Bright blue
COLOR_PROGRESS_BAR_SUBPROGRESS          = 0xFFB1; # Dark blue on bright cyan

CONSOLE_UNDERLINE                       = 0x10000;

# COMMONLY USED CHARS
CHAR_INFO                               = "→";
CHAR_LIST                               = "•";

CHAR_BUSY                               = "»";
CHAR_OK                                 = "√";
CHAR_WARNING                            = "▲";
CHAR_ERROR                              = "×";

CHAR_SELECT_YES                         = "●";
CHAR_SELECT_MAYBE                       = "•";
CHAR_SELECT_NO                          = "·";

CHAR_INPUT                              = "►";
CHAR_OUTPUT                             = "◄";

CHAR_ADD                                = "+";
CHAR_MODIFY                             = "±";
CHAR_REMOVE                             = "-";
CHAR_IGNORE                             = "·";

# DEFAULTS
from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();
oConsole.uDefaultColor = COLOR_NORMAL;
oConsole.uDefaultBarColor = COLOR_PROGRESS_BAR;
oConsole.uDefaultProgressColor = COLOR_PROGRESS_BAR_HILITE;
oConsole.uDefaultSubProgressColor = COLOR_PROGRESS_BAR_SUBPROGRESS;

# APPLICATION SPECIFIC COLOR NAMES
COLOR_REQUEST_RESPONSE_BOX              = 0xFF08;
COLOR_REQUEST_RESPONSE_BOX_HEADER       = 0xFF80;

COLOR_REQUEST_STATUS_LINE               = 0xFF0E; # Yellow
COLOR_RESPONSE_STATUS_LINE_1XX          = 0xFF0F; # White
COLOR_RESPONSE_STATUS_LINE_2XX          = 0xFF0A; # Bright green
COLOR_RESPONSE_STATUS_LINE_3XX          = 0xFF0B; # Bright cyan
COLOR_RESPONSE_STATUS_LINE_4XX          = 0xFF0C; # Bright red
COLOR_RESPONSE_STATUS_LINE_5XX          = 0xFF0D; # Bright purple
COLOR_RESPONSE_STATUS_LINE_INVALID      = 0xFF04; # Red

COLOR_HEADER_NAME                       = 0xFF09; # Bright blue
COLOR_HEADER_VALUE                      = 0xFF0B; # Bright 

COLOR_BODY_DECODED                      = 0xFF07;
COLOR_BODY                              = 0xFF07;

COLOR_CR                                = 0xFF08;
COLOR_LF                                = 0xFF08;
COLOR_CRLF                              = 0xFF08;
COLOR_EOF                               = 0xFF08;

COLOR_ACTIVE                            = 0xFF0F;
COLOR_INACTIVE                          = 0xFF08;
COLOR_NOTHING                           = 0xFF08;
COLOR_CONNECT                           = 0xFF02;
COLOR_CONNECTED                         = 0xFF0A;
COLOR_DISCONNECTED                      = 0xFF0C;
COLOR_REQUEST                           = 0xFF0E;
COLOR_RESPONSE_1XX                      = 0xFF0F; # White
COLOR_RESPONSE_2XX                      = 0xFF0A; # Bright green
COLOR_RESPONSE_3XX                      = 0xFF0B; # Bright cyan
COLOR_RESPONSE_4XX                      = 0xFF0C; # Bright red
COLOR_RESPONSE_5XX                      = 0xFF0D; # Bright purple
COLOR_RESPONSE_INVALID                  = 0xFF04; # Red

# APPLICATION SPECIFIC CHARS
CHAR_CR                                 = "←";
CHAR_LF                                 = "↓";
CHAR_CRLF                               = "←┘";
CHAR_EOF                                = "×";

