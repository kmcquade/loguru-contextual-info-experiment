import sys
from os import environ
from contextvars import ContextVar
from loguru import logger
import copy

# Store context variables in a dictionary
context_vars = {}


# taken from Loguru but with the addition of the extra field
def env(key, type_, default=None):
    if key not in environ:
        return default

    val = environ[key]

    if type_ == str:
        return val
    if type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    if type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None
    raise ValueError("The requested type '%r' is not supported" % type_)


def bind_context_to_logger(**kwargs):
    """
    Bind arbitrary key-value pairs to the logger's context.
    """
    global context_vars

    # For each key-value pair, set the context variable and update the global context_vars
    for key, value in kwargs.items():
        if key not in context_vars:
            # Create a new ContextVar for the key if it doesn't exist
            context_var = ContextVar(key)
            context_vars[key] = context_var
        else:
            # Retrieve existing ContextVar
            context_var = context_vars[key]

        # Set the value for the context variable
        context_var.set(value)

    # Patch logger to include all context variables in its extra
    def patcher(record):
        extras = copy.deepcopy(record["extra"])
        for key, context_var in context_vars.items():
            extras[key] = context_var.get()
        record["extra"].update(extras)

    logger.configure(patcher=patcher)


LOG_FORMAT = env(
    "LOGURU_FORMAT",
    str,
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | {extra}",
)


def init_logger(environment_name: str):
    # Remove all existing handlers
    logger.remove()
    stdout_handler = {
        "sink": sys.stdout,
        "serialize": False,
        "level": "DEBUG",
        "format": LOG_FORMAT,
    }
    logger.add(**stdout_handler)
    bind_context_to_logger(environment_name=environment_name)
