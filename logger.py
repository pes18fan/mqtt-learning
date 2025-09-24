# logger.py
import logging

logger = logging.getLogger(__name__)       # module-level logger
logger.setLevel(logging.INFO)              # default level

_handler = logging.StreamHandler()         # console
_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s:%(lineno)d: %(message)s"
))
logger.addHandler(_handler)
