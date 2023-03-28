import logging

from src.meta import Desktop
from src.plugins._plugin import Plugin, PluginDesktopDependent, PluginCommandline
from src.plugins.system import test_gnome_availability

logger = logging.getLogger(__name__)


class Icon(PluginDesktopDependent):
    name = 'Icon'

    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.KDE:
                super().__init__(_Kde())
            case Desktop.GNOME:
                super().__init__(_Gnome())
            case Desktop.XFCE:
                super().__init__(_Xfce())
            case _:
                super().__init__(None)

    @property
    def available_themes(self) -> dict:
        themes = []

        for directory in theme_directories:
            if not path.isdir(directory):
                continue

            with scandir(directory) as entries:
                themes.extend(d.name for d in entries if d.is_dir() and path.isdir(d.path + '/gtk-3.0'))

        return {t: t for t in themes}


class _Gnome(PluginCommandline):
    name = 'Icon'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.desktop.interface', 'icon-theme', '{theme}'])
        self.theme_light = 'Default'
        self.theme_dark = 'Default'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Kde(Plugin):
    name = 'Icon'

    def __init__(self):
        super().__init__()
        self.theme_light = 'breeze'
        self.theme_dark = 'breeze-dark'

    def apply_theme(self, theme: str) -> bool:
        logger.info(f'Applying icon theme {theme}')
        return self._apply_theme(theme)

    def _apply_theme(self, theme: str) -> bool:
        try:
            process = subprocess.run(
                ['kwriteconfig5', '--file', 'kdeglobals', '--group', 'Icons', '--key', 'Theme', theme],
                stdout=subprocess.DEVNULL
            )
            return process.returncode == 0
        except FileNotFoundError:
            return False

class _Xfce(PluginCommandline):
    name = 'Icon'

    def __init__(self):
        super().__init__(['xfconf-query', '-c', 'xsettings', '-p', '/Net/IconThemeName', '-s', '{theme}'])
        self.theme_light = 'Default'
        self.theme_dark = 'Default'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)
