import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "query_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "query.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["query_handler"],
            "level": "DEBUG",
        },
    },
}