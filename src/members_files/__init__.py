"""Initialise the application."""
from psiutils.utilities import psi_logger
from members_files.constants import APP_NAME

from ._version import __version__

version = __version__

logger = psi_logger(APP_NAME)
