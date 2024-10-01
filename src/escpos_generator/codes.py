import re
from dataclasses import dataclass
from enum import Enum, auto

from escpos.constants import QR_ECLEVEL_H, QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q
from typing_extensions import deprecated


class _BarcodeType(Enum):
    CODE39 = auto()
    CODE128 = auto()


class BarcodeCodePage(Enum):
    a = "{A"
    b = "{b"
    c = "{c"


class Barcode:
    @deprecated("Use constructor methods like `Barcode.code128`")
    def __init__(self, data: str, type: _BarcodeType, height: int, width: int):
        Barcode._check_h_w(height, width)
        self.data = data
        self.type = type
        self.height = height
        self.width = width

    _default_height = 162
    _default_width = 3

    @staticmethod
    def code39(
        data: str,
        height: int = _default_height,
        width: int = _default_width,
    ) -> "Barcode":
        Barcode._check_h_w(height, width)
        if not (1 <= len(data) <= 255):
            raise ValueError("Barcode: Wrong data range. 1 < k < 255")

        if re.match(r"^[0-9A-Z \$\%\*\+\-\.\/]$", data):
            raise ValueError("Barcode: Data is not valid")

        return Barcode(
            data=data,
            type=_BarcodeType.CODE39,
            height=height,
            width=width,
        )

    @staticmethod
    def code128(
        data: str,
        code_page: BarcodeCodePage = BarcodeCodePage.a,
        height: int = _default_height,
        width: int = _default_width,
    ) -> "Barcode":
        Barcode._check_h_w(height, width)

        if not (2 <= len(data) <= 255):
            raise ValueError("Barcode: Wrong data range. 2 < n < 255")

        for char in data:
            if ord(char) > 127:
                raise ValueError("Barcode: Data is not valid")

        return Barcode(
            data=code_page.value + data,
            type=_BarcodeType.CODE128,
            height=height,
            width=width,
        )

    def __post_init__(self):
        Barcode._check_h_w(self.height, self.width)

    @staticmethod
    def _check_h_w(height: int, width: int) -> None:
        if not 1 <= height <= 255:
            raise ValueError("Barcode: height out of range")
        if not 2 <= width <= 6:
            raise ValueError("Barcode: width out of range")


class QRSize(Enum):
    s1 = 1
    s2 = 2
    s3 = 3
    s4 = 4
    s5 = 5
    s6 = 6
    s7 = 7
    s8 = 8
    s9 = 9
    s10 = 10
    s11 = 11
    s12 = 12
    s13 = 13
    s14 = 14
    s15 = 15
    s16 = 16


class QRCorrection(Enum):
    l = QR_ECLEVEL_L
    m = QR_ECLEVEL_M
    q = QR_ECLEVEL_Q
    h = QR_ECLEVEL_H


@dataclass
class QRCode:
    data: str
    size: QRSize = QRSize.s4
    correction: QRCorrection = QRCorrection.l
