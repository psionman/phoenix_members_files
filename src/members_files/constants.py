"""Constants for Phoenix Members Files."""
from pathlib import Path
from appdirs import user_config_dir, user_data_dir

from psiutils.known_paths import resolve_path

# General
AUTHOR = 'Jeff Watkins'
APP_NAME = 'phoenix_members'
APP_AUTHOR = 'psionman'
HTML_DIR = resolve_path('html', __file__)
HELP_URI = ''

# Paths
CONFIG_PATH = Path(user_config_dir(APP_NAME, APP_AUTHOR), 'config.toml')
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
USER_DATA_FILE = 'members.json'
HOME = str(Path.home())

# GUI
APP_TITLE = 'Phoenix Members Files'
ICON_FILE = resolve_path(Path('images', 'icon.png'), __file__)
DEFAULT_GEOMETRY = '400x500'
