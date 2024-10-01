from dataclasses import dataclass
from enum import Enum, auto

from escpos.constants import QR_ECLEVEL_H, QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q


class BarcodeType(Enum):
    CODE39 = auto()
    CODE128 = auto()


@dataclass
class Barcode:
    type: BarcodeType
    data: str
    height: int = 162
    width: int = 3

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
