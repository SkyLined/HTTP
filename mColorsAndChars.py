# COMMONLY USED COLOR NAMES
COLOR_DIM                               = 0xFF08; # Dark gray
COLOR_NORMAL                            = 0xFF07; # Light gray
COLOR_HILITE                            = 0xFF0B; # Bright cyan

COLOR_INFO                              = 0xFF0F; # 
COLOR_LIST                              = 0xFF0F; # White

COLOR_BUSY                              = 0xFF03; # Cyan
COLOR_OK                                = 0xFF02; # Green
COLOR_WARNING                           = 0xFF06; # Brown
COLOR_ERROR                             = 0xFF04; # Red

COLOR_SELECT_YES                        = 0xFF09; # Bright blue
COLOR_SELECT_MAYBE                      = 0xFF09; # Bright blue
COLOR_SELECT_NO                         = 0xFF09; # Bright blue

COLOR_INPUT                             = 0xFF0B; #
COLOR_OUTPUT                            = 0xFF07; #

COLOR_ADD                               = 0xFF0A; # Bright green
COLOR_MODIFY                            = 0xFF0B; # Bright cyan
COLOR_REMOVE                            = 0xFF0C; # Bright red

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
COLOR_REQUEST_RESPONSE_BOX_HEADER       = 0xFF08;

COLOR_REQUEST_STATUS_LINE               = 0xFF8F; # White on dark grey
COLOR_RESPONSE_STATUS_LINE_1XX          = 0xFF3F; # White on cyan
COLOR_RESPONSE_STATUS_LINE_2XX          = 0xFF2F; # White on green
COLOR_RESPONSE_STATUS_LINE_3XX          = 0xFF6F; # White on brown
COLOR_RESPONSE_STATUS_LINE_4XX          = 0xFF4F; # White on red
COLOR_RESPONSE_STATUS_LINE_5XX          = 0xFF5F; # White on purple
COLOR_RESPONSE_STATUS_LINE_INVALID      = 0xFFC0; # Black on bright red

COLOR_HEADER_NAME                       = 0xFF0B; # Bright cyan
COLOR_HEADER_VALUE                      = 0xFF07; # Bright grey

COLOR_BODY                              = 0xFF07;
COLOR_DATA                              = 0xFF0F;

COLOR_CR                                = 0xFF0E;
COLOR_LF                                = 0xFF0A;
COLOR_CRLF                              = 0xFF0F;
COLOR_EOF                               = 0xFF0C;

COLOR_ACTIVE                            = 0xFF0F;
COLOR_INACTIVE                          = 0xFF08;
COLOR_NOTHING                           = 0xFF08;
COLOR_CONNECT                           = 0xFF02;
COLOR_CONNECTED                         = 0xFF0A;
COLOR_DISCONNECTED                      = 0xFF0C;
COLOR_REQUEST                           = 0xFF0E; # White
COLOR_RESPONSE_1XX                      = 0xFF0B; # Bright cyan
COLOR_RESPONSE_2XX                      = 0xFF0A; # Bright green
COLOR_RESPONSE_3XX                      = 0xFF0E; # Yellow
COLOR_RESPONSE_4XX                      = 0xFF0C; # Bright red
COLOR_RESPONSE_5XX                      = 0xFF0D; # Bright purple
COLOR_RESPONSE_INVALID                  = 0xFF04; # Red

# APPLICATION SPECIFIC CHARS
CHAR_CR                                 = "←";
CHAR_LF                                 = "↓";
CHAR_CRLF                               = "←┘";
CHAR_EOF                                = "×";

