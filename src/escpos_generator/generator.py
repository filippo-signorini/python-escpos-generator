import logging
import time
from math import floor
from typing import Optional

from escpos.exceptions import DeviceNotFoundError, USBNotFoundError
from escpos.printer import Usb
from typing_extensions import assert_never
from usb import USBError

from .codes import Barcode, QRCode
from .enums import PosPaperSize
from .style import PosAlign, PosFontType, PosStyle

logging.basicConfig()
logger = logging.getLogger(__name__)


class Generator:
    def __init__(
        self,
        idVendor: int,
        idProduct: int,
        paper_size: PosPaperSize,
        debug=False,
    ) -> None:
        self._id_vendor = idVendor
        self._id_product = idProduct
        self.paper_size = paper_size
        self._currentStyle = PosStyle.defaults()
        self.p = Usb(self._id_vendor, self._id_product)

    def check_usb(self) -> bool:
        try:
            self.p.buzzer()
        except (USBNotFoundError, DeviceNotFoundError, USBError):
            logger.error("Stampante non trovata, tento riconnessione")
            conn = False
            max_tries = 2
            for i in range(max_tries):
                try:
                    self.p.open()
                except (USBNotFoundError, DeviceNotFoundError):
                    if i + 1 < max_tries:
                        time.sleep(5)
                else:
                    conn = True
                    break

            if conn:
                logger.info("Stampante riconnessa")
            else:
                logger.warning("Impossibile connettersi alla stampante, salto")
            return conn
        else:
            return True

    @property
    def max_chars_per_line(self) -> int:
        font = self._currentStyle.font_type
        if self.paper_size is PosPaperSize.mm58:
            return 32 if font is None or font is PosFontType.fontA else 42
        elif self.paper_size is PosPaperSize.mm80:
            return 48 if font is None or font is PosFontType.fontA else 64
        assert_never(self.paper_size)

    def init(self) -> None:
        if not self.check_usb():
            return

        self.p.hw("INIT")
        self._set_style(self._currentStyle)

    def _set_style(self, style: PosStyle) -> None:
        if not self.check_usb():
            return

        self.p.set(
            align=style.align.name if style.align is not None else None,
            bold=style.bold,
            custom_size=True if style.height or style.width else False,
            double_height=style.double_height,
            double_width=style.double_width,
            flip=style.upside_down,
            underline=style.underline,
            density=None,
            font=style.font_type.value if style.font_type is not None else None,
            height=style.height.value if style.height is not None else None,
            width=style.width.value if style.width is not None else None,
            invert=style.inverted,
            normal_textsize=not style.double_height and not style.double_width,
        )

    def text(
        self,
        text: str,
        lines_after: int = 1,
        style: Optional[PosStyle] = None,
        keep_style: bool = False,
    ) -> None:
        if not self.check_usb():
            return

        if style is not None:
            self._set_style(style.merge(self._currentStyle, allow_null=True))
            if keep_style:
                self._currentStyle = style.merge(self._currentStyle, allow_null=False)

        self.p.text(text)
        if lines_after > 0:
            self.empty_lines(lines_after)
        if style is not None and not keep_style:
            self._set_style(self._currentStyle.merge(style, allow_null=True))

    def cut(self) -> None:
        if not self.check_usb():
            return

        self.p.cut(feed=False)

    def empty_lines(self, lines: int = 1) -> None:
        if not self.check_usb():
            return

        if lines > 0:
            self.p.ln(lines)

    def hr(self, half: bool = False) -> None:
        if not self.check_usb():
            return

        line = "-" * floor(
            self.max_chars_per_line / 2 if half else self.max_chars_per_line
        )
        self.text(line, style=PosStyle(align=PosAlign.center))

    def set_style(self, style: PosStyle) -> None:
        if not self.check_usb():
            return

        self._set_style(style.merge(self._currentStyle, allow_null=True))
        self._currentStyle = style.merge(self._currentStyle, allow_null=False)

    def qr(self, qr_code: QRCode) -> None:
        if not self.check_usb():
            return

        self.p.qr(
            qr_code.data,
            ec=qr_code.correction.value,
            size=qr_code.size.value,
            center=True,
        )

    def barcode(self, barcode: Barcode) -> None:
        if not self.check_usb():
            return

        self.p.barcode(
            barcode.data,
            bc=barcode.type.name,
            height=barcode.height,
            width=barcode.width,
            align_ct=True,
            pos="OFF",
        )

    def image(self, image: str, align: PosAlign = PosAlign.center) -> None:
        if not self.check_usb():
            return

        self._set_style(PosStyle(align=align))
        self.p.image(image)
        self._set_style(self._currentStyle)

    def test_page(self):
        if not self.check_usb():
            return

        self.empty_lines()
        self.text("   0 1 2 3 4 5 6 7 8 9 A B C D E F ")
        self.empty_lines()
        for i in range(0, 0x10):
            self.text(hex(i)[2:].upper(), lines_after=0)
            for j in range(0, 0x10):
                digit = max(i * 0x10 + j, 0x20)
                self.text(chr(digit) + " ", lines_after=0)
            self.empty_lines()
        self.cut()
