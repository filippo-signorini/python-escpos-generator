from enum import Enum

from typing_extensions import assert_never


class PosPaperSize(Enum):
    mm58 = 0
    mm80 = 0

    @property
    def width(self) -> int:
        if self is PosPaperSize.mm58:
            return 372
        elif self is PosPaperSize.mm80:
            return 558
        assert_never(self)
