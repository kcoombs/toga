from __future__ import annotations

# Use the Travertino font definitions as-is
from travertino import constants
from travertino.constants import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
)
from travertino.fonts import Font as BaseFont

import toga
from toga.platform import get_platform_factory

SYSTEM_DEFAULT_FONTS = {SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE}
SYSTEM_DEFAULT_FONT_SIZE = -1
FONT_WEIGHTS = {NORMAL, BOLD}
FONT_STYLES = {NORMAL, ITALIC, OBLIQUE}
FONT_VARIANTS = {NORMAL, SMALL_CAPS}

_REGISTERED_FONT_CACHE = {}


class Font(BaseFont):
    def __init__(
        self,
        family: str,
        size: int | str,
        *,
        weight: str = NORMAL,
        style: str = NORMAL,
        variant: str = NORMAL,
    ):
        """This class is used to represent a font when drawing on a :any:`Canvas`. For
        all other widgets, fonts can be controlled using the style properties which are
        linked below.

        :param family: The :ref:`font family <pack-font-family>`.
        :param size: The :ref:`font size <pack-font-size>`.
        :param weight: The :ref:`font weight <pack-font-weight>`.
        :param style: The :ref:`font style <pack-font-style>`.
        :param variant: The :ref:`font variant <pack-font-variant>`.
        """
        super().__init__(family, size, weight=weight, style=style, variant=variant)
        self.factory = get_platform_factory()
        self._impl = self.factory.Font(self)

    def __str__(self) -> str:
        size = (
            "default size"
            if self.size == SYSTEM_DEFAULT_FONT_SIZE
            else f"{self.size}pt"
        )
        weight = f" {self.weight}" if self.weight != NORMAL else ""
        variant = f" {self.variant}" if self.variant != NORMAL else ""
        style = f" {self.style}" if self.style != NORMAL else ""
        return f"{self.family} {size}{weight}{variant}{style}"

    @staticmethod
    def register(family, path, *, weight=NORMAL, style=NORMAL, variant=NORMAL):
        """Registers a file-based font.

        **Note:** This is not currently supported on macOS or iOS.

        When invalid values for style, variant or weight are passed, ``NORMAL`` will be
        used.

        When a font includes multiple weights, styles or variants, each one must be
        registered separately, even if they're stored in the same file::

            from toga.style.pack import BOLD

            # Register a simple regular font
            Font.register(
                "Font Awesome 5 Free Solid", "Font Awesome 5 Free-Solid-900.otf"
            )

            # Register a regular and bold font, contained in separate font files
            Font.register("Roboto", "Roboto-Regular.ttf")
            Font.register("Roboto", "Roboto-Bold.ttf", weight=BOLD)

            # Register a single font file that contains both a regular and bold weight
            Font.register("Bahnschrift", "Bahnschrift.ttf")
            Font.register("Bahnschrift", "Bahnschrift.ttf", weight=BOLD)

        Parameters are the same as in the ``Font`` constructor above, with the addition
        of:

        :param path: The path to the font file. This can be an absolute path, or a path
            relative to the module that defines your :any:`App` class.
        """
        font_key = Font._registered_font_key(family, weight, style, variant)
        _REGISTERED_FONT_CACHE[font_key] = str(toga.App.app.paths.app / path)

    @staticmethod
    def _registered_font_key(family, weight, style, variant):
        if weight not in constants.FONT_WEIGHTS:
            weight = NORMAL
        if style not in constants.FONT_STYLES:
            style = NORMAL
        if variant not in constants.FONT_VARIANTS:
            variant = NORMAL

        return family, weight, style, variant
