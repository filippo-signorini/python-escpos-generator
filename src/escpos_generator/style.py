from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypeVar


class PosFontType(Enum):
    fontA = "a"
    fontB = "b"


class PosAlign(Enum):
    left = "left"
    center = "center"
    right = "right"


class PosRotation(Enum):
    r0 = 0
    r90 = 1


class PosTextSize(Enum):
    size1 = 1
    size2 = 2
    size3 = 3
    size4 = 4
    size5 = 5
    size6 = 6
    size7 = 7
    size8 = 8


@dataclass
class PosStyle:
    bold: Optional[bool] = None
    double_height: Optional[bool] = None
    double_width: Optional[bool] = None
    height: Optional[PosTextSize] = None
    width: Optional[PosTextSize] = None
    underline: Optional[bool] = None
    align: Optional[PosAlign] = None
    font_type: Optional[PosFontType] = None
    italic: Optional[bool] = None
    upside_down: Optional[bool] = None
    rotation: Optional[PosRotation] = None
    inverted: Optional[bool] = None

    _T = TypeVar("_T")

    @staticmethod
    def defaults() -> "PosStyle":
        return PosStyle(
            bold=False,
            double_height=False,
            double_width=False,
            underline=False,
            align=PosAlign.left,
            font_type=PosFontType.fontA,
            italic=False,
            upside_down=False,
            inverted=False,
        )

    def merge(self, other: "PosStyle", allow_null: bool) -> "PosStyle":
        return PosStyle(
            bold=self._get_par(self.bold, other.bold, allowNull=allow_null),
            double_height=self._get_par(
                self.double_height, other.double_height, allowNull=allow_null
            ),
            double_width=self._get_par(
                self.double_width, other.double_width, allowNull=allow_null
            ),
            height=self._get_par(self.height, other.height, allowNull=allow_null),
            width=self._get_par(self.width, other.width, allowNull=allow_null),
            underline=self._get_par(
                self.underline, other.underline, allowNull=allow_null
            ),
            align=self._get_par(self.align, other.align, allowNull=allow_null),
            font_type=self._get_par(
                self.font_type, other.font_type, allowNull=allow_null
            ),
            italic=self._get_par(self.italic, other.italic, allowNull=allow_null),
            upside_down=self._get_par(
                self.upside_down, other.upside_down, allowNull=allow_null
            ),
            rotation=self._get_par(self.rotation, other.rotation, allowNull=allow_null),
            inverted=self._get_par(self.inverted, other.inverted, allowNull=allow_null),
        )

    def _get_par(
        self, par: Optional[_T], defaultValue: Optional[_T], allowNull: bool = True
    ) -> Optional[_T]:
        if par != defaultValue:
            return par if par is not None else defaultValue

        if allowNull:
            return None
        return defaultValue
