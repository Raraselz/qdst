class zcolors:

    """ BACKGROUND AND FOREGROUND """

    BG_BLACK = '\033[40m'
    FG_BLACK = '\033[30m'

    BG_DARKRED = '\033[41m'
    FG_DARKRED = '\033[31m'

    BG_DARKGREEN = '\033[42m'
    FG_DARKGREEN = '\033[32m'

    BG_DARKYELLOW = '\033[43m'
    FG_DARKYELLOW = '\033[33m'

    BG_DARKBLUE = '\033[44m'
    FG_DARKBLUE = '\033[34m'

    BG_DARKMAGENTA = '\033[45m'
    FG_DARKMAGENTA = '\033[35m'

    BG_DARKCYAN = '\033[46m'
    FG_DARKCYAN = '\033[36m'

    BG_DARKGREY = '\033[100m'
    FG_DARKGREY = '\033[90m'

    BG_LIGHTGREY = '\033[47m'
    FG_LIGHTGREY = '\033[37m'

    BG_LIGHTRED = '\033[101m'
    FG_LIGHTRED = '\033[91m'

    BG_LIGHTRED = '\033[101m'
    FG_LIGHTRED = '\033[91m' # FAIL

    BG_LIGHTGREEN = '\033[102m'
    FG_LIGHTGREEN = '\033[92m' # OKGREEN

    BG_LIGHTYELLOW = '\033[103m'
    FG_LIGHTYELLOW = '\033[93m' # WARNING

    BG_LIGHTBLUE = '\033[104m'
    FG_LIGHTBLUE = '\033[94m' # OKBLUE

    BG_LIGHTMAGENTA = '\033[105m'
    FG_LIGHTMAGENTA = '\033[95m' # HEADER

    BG_LIGHTCYAN = '\033[106m'
    FG_LIGHTCYAN = '\033[96m' # OKCYAN

    BG_WHITE = '\033[107m'
    FG_WHITE = '\033[97m'

    """
            GENERAL FORMATTING
       ! Likely not going to work on !
            ! most terminals !
    """

    BOLD = '\033[1m' # BOLD
    UNDERLINE = '\033[4m' # UNDERLINE
    NO_UNDERLINE = '\033[24m'
    REVERSE = '\033[7m'
    NO_REVERSE = '\033[27m'

    """
            ~ RESET ~
        USE THIS AT THE END OF EVERY PRINT STATEMENT THAT USES COLORS
    """

    X = '\033[0m' # ENDC

    """
        ORIGINAL CREATOR: tuvokki on GitHub
        ZCOLORS (BCOLORS v 2.0) by ZENGULETZ
    """