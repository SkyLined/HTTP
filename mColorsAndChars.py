# COMMONLY USED COLOR NAMES
COLOR_DIM                               = 0xFF08; # Dark gray
COLOR_NORMAL                            = 0xFF07; # Light gray
COLOR_HILITE                            = 0xFF0B; # Bright cyan

COLOR_INFO                              = 0xFF0F; # 
COLOR_LIST                              = 0xFF0F; # White

COLOR_BUSY                              = 0xFF03; # Cyan
COLOR_OK                                = 0xFF02; # Green
COLOR_WARNING                           = 0xFF06; # Brown
COLOR_ERROR                             = 0xFF0C; # Red

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
CHAR_OK                                 = "✓";
CHAR_WARNING                            = "▲";
CHAR_ERROR                              = "✘";

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
COLOR_DATA                              = 0xFF07;

COLOR_CR                                = 0xFF08;
COLOR_LF                                = 0xFF08;
COLOR_CRLF                              = 0xFF08;
COLOR_EOF                               = 0xFF04;

COLOR_ACTIVE                            = 0xFF0F;
COLOR_INACTIVE                          = 0xFF08;
COLOR_NOTHING                           = 0xFF08;
COLOR_SPOOFED                           = 0xFF06;
COLOR_RESOLVING                         = 0xFF02;
COLOR_RESOLVED                          = 0xFF0A;
COLOR_CONNECTING                        = 0xFF02;
COLOR_CONNECTED                         = 0xFF0A;
COLOR_DISCONNECTED                      = 0xFF0C;
COLOR_SECURING                          = 0xFF02;
COLOR_SECURED                           = 0xFF0A;
COLOR_REQUEST                           = 0xFF0E; # White
COLOR_RESPONSE                          = 0xFF0E; # White (used before we know the status code)
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

CHAR_SPOOFED                            = "→";
STR_SPOOFED3                            = "··→";
CHAR_RESOLVING                          = "→";
STR_RESOLVING3                          = "··→";
CHAR_RESOLVING_ERROR                    = "✘";
STR_RESOLVING_ERROR3                    = "→✘ ";
CHAR_RESOLVED                           = "·";
STR_RESOLVED3                           = "··→";

CHAR_CONNECTING_FROM                    = "←";
STR_CONNECTING_FROM3                    = "←--";
CHAR_CONNECTED_FROM                     = "←"
STR_CONNECTED_FROM3                     = "←――"

CHAR_CONNECTING_TO                      = "→";
STR_CONNECTING_TO3                      = "--→";
CHAR_CONNECTED_TO                       = "→";
STR_CONNECTED_TO3                       = "――→";

CHAR_CONNECTING_TO_ERROR                = "✘"
STR_CONNECTING_TO_ERROR3                = "→✘ ";

CHAR_DISCONNECTED                       = "×"
STR_DISCONNECTED3                       = "-×-";

CHAR_SECURING                           = "↔";
STR_SECURING3                           = "←-→";
CHAR_SECURING_ERROR                     = "✘";
STR_SECURING_ERROR3                     = "←✘→"
CHAR_SECURED                            = "═";
STR_SECURED3                            = "═══";

CHAR_SENDING_REQUEST                    = ">";
STR_SENDING_REQUEST3                    = "――>";
CHAR_SENDING_REQUEST_SECURELY           = "►";
STR_SENDING_REQUEST_SECURELY3           = "══>";
CHAR_SENDING_REQUEST_ERROR              = "►";
STR_SENDING_REQUEST_ERROR3              = "══>";
CHAR_SENDING_REQUEST_SECURELY_ERROR     = "✘";
STR_SENDING_REQUEST_SECURELY_ERROR3     = "═>✘";
CHAR_REQUEST_SENT                       = ">";
STR_REQUEST_SENT3                       = "――>";
CHAR_REQUEST_SENT_SECURELY              = "►";
STR_REQUEST_SENT_SECURELY3              = "══>";

CHAR_RECEIVING_REQUEST                  = "<";
STR_RECEIVING_REQUEST3                  = "<――";
CHAR_RECEIVING_REQUEST_SECURELY         = "◄";
STR_RECEIVING_REQUEST_SECURELY3         = "<══";
CHAR_RECEIVING_REQUEST_ERROR            = "✘";
STR_RECEIVING_REQUEST_ERROR3            = "✘<―";
CHAR_RECEIVING_REQUEST_SECURELY_ERROR   = "✘";
STR_RECEIVING_REQUEST_SECURELY_ERROR3   = "✘<═";
CHAR_REQUEST_RECEIVED                   = "<";
STR_REQUEST_RECEIVED3                   = "<――";
CHAR_REQUEST_RECEIVED_SECURELY          = "◄";
STR_REQUEST_RECEIVED_SECURELY3          = "<══";

CHAR_SENDING_RESPONSE                   = ">";
STR_SENDING_RESPONSE3                   = "――>";
CHAR_SENDING_RESPONSE_SECURELY          = "►";
STR_SENDING_RESPONSE_SECURELY3          = "══>";
CHAR_SENDING_RESPONSE_ERROR             = "✘";
STR_SENDING_RESPONSE_ERROR3             = "―>✘";
CHAR_SENDING_RESPONSE_SECURELY_ERROR    = "✘";
STR_SENDING_RESPONSE_SECURELY_ERROR3    = "═>✘";
CHAR_RESPONSE_SENT                      = ">";
STR_RESPONSE_SENT3                      = "――>";
CHAR_RESPONSE_SENT_SECURELY             = "►";
STR_RESPONSE_SENT_SECURELY3             = "══>";

CHAR_RECEIVING_RESPONSE                 = "<";
STR_RECEIVING_RESPONSE3                 = "<――";
CHAR_RECEIVING_RESPONSE_SECURELY        = "◄";
STR_RECEIVING_RESPONSE_SECURELY3        = "<══";
CHAR_RECEIVING_RESPONSE_ERROR           = "✘";
STR_RECEIVING_RESPONSE3_ERROR           = "✘<―";
CHAR_RECEIVING_RESPONSE_SECURELY_ERROR  = "✘";
STR_RECEIVING_RESPONSE_SECURELY_ERROR3  = "✘<═";
CHAR_RESPONSE_RECEIVED                  = "<";
STR_RESPONSE_RECEIVED3                  = "<――";
CHAR_RESPONSE_RECEIVED_SECURELY         = "◄";
STR_RESPONSE_RECEIVED_SECURELY3         = "<══";
