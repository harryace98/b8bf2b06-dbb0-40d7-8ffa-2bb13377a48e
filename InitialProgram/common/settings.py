
DEBUG = 10
INFO = 20
SUCCESS = 25
WARNING = 30
ERROR = 40

DEFAULT_LEVELS = {
    'DEBUG': DEBUG,
    'INFO': INFO,
    'SUCCESS': SUCCESS,
    'WARNING': WARNING,
    'ERROR': ERROR,
}

# SERVER_ERROR_TIMER=60
# SERVER_PORT = '5004'
#LOG_DIR = '/var/log'
LOG_DIR = './logs/'
LOG_FILE = LOG_DIR+'/program.log'
LOG_FORMAT = '%(asctime)s [%(lineno)d] PID:%(process)d %(name)s %(levelname)s: %(message)s'
CONSOLE_LOG_FORMAT = '%(asctime)s [%(lineno)d] PID:%(process)d %(name)s %(levelname)s: %(message)s'
FILE_LOG_LEVEL = 'DEBUG'
CONSOLE_LOG_LEVEL = 'DEBUG'

## internet Watch Dog Setting
RESTART_FILE_NAME = 'restarts.csv'
RESTART_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
URL_TARGET = "a39g730csmjomc-ats.iot.us-east-1.amazonaws.com"
INTERFACE_TARGET = "eth0"
TIMETOEXEC = 900