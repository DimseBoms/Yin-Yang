import json
from pathlib import Path

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton

from src.plugins._plugin import Plugin, get_int_from_qcolor

PATH = f'{Path.home()}/.config/BraveSoftware/Brave-Browser/Default/Preferences'


class Brave(Plugin):
    def __init__(self):
        super().__init__()
        self.theme_light = '#ffffff'
        self.theme_dark = '#000000'

    def set_theme(self, color_str: str):
        with open(PATH, 'r') as file:
            config = json.load(file)

        color = get_int_from_qcolor(QColor(color_str))
        config['autogenerated']['theme']['color'] = color

    def get_input(self, widget):
        widgets = []

        for theme in ['Light', 'Dark']:
            grp = QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            line = QLineEdit(grp)
            horizontal_layout.addWidget(line)

            btn = QPushButton()
            btn.setText(f'Pick {theme} color')
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets