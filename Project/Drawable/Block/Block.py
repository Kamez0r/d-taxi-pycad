from abc import abstractmethod
from contextlib import suppress

from PyQt6.QtCore import QRectF, QLineF, Qt
from PyQt6.QtGui import QColor, QPen, QFont, QFontMetrics

from Project import Drawable


class Block(Drawable):

    def __init__(self):
        super().__init__()
        self.width = 500
        self.height = 500

        self.penWidth = 2
        self.penColor = QColor(255, 0, 0)

        self.minFontHeight = int(self.height / 32)
        self.maxFontHeight = int(self.height / 4)


        self.header_text = "No Header Text"
        self.title_text = "No Title Text"
        self.footer_text = "No Footer Text"

    def boundingRect(self):
        return QRectF((-self.width / 2) - self.penWidth / 2, (-self.height / 2) - self.penWidth / 2,
                      self.width + self.penWidth, self.height + self.penWidth)

    def paint(self, painter, option, widget):
        my_pen = QPen()
        my_pen.setColor(self.penColor)
        my_pen.setWidth(self.penWidth)

        painter.setPen(my_pen)

        the_font = QFont('Consolas', 50)
        painter.setFont(the_font)

        # Bounding Rectangle
        painter.drawRect(self.boundingRect())

        # < Header >
        self.paint_header(painter, option, widget, QRectF(
            -self.width / 2, (-self.height / 2) + (0 * self.height),
            self.width, 0.2 * self.height
        ))

        # Divider / Header <> Graphics
        percent_ratio = 0.2
        painter.drawLine(QLineF(
            -self.width/2, (-self.height/2)+(percent_ratio * self.height),
            self.width/2,  (-self.height/2)+(percent_ratio * self.height)
        ))

        # < Graphics >
        self.paint_graphics(painter, option, widget, QRectF(
            -self.width / 2, (-self.height / 2) + (percent_ratio * self.height),
            self.width, 0.4 * self.height
        ))

        # Divider / Graphics <> Title
        percent_ratio = 0.6
        painter.drawLine(QLineF(
            -self.width/2, (-self.height/2)+(percent_ratio * self.height),
            self.width/2,  (-self.height/2)+(percent_ratio * self.height)
        ))

        # < Title >
        self.paint_title(painter, option, widget, QRectF(
            -self.width / 2, (-self.height / 2) + (percent_ratio * self.height),
            self.width, 0.2 * self.height
        ))

        # Divider / Title <> Footer
        percent_ratio = 0.8
        painter.drawLine(QLineF(
            -self.width/2, (-self.height/2)+(percent_ratio * self.height),
            self.width/2,  (-self.height/2)+(percent_ratio * self.height)
        ))

        # < Footer >
        self.paint_footer(painter, option, widget, QRectF(
            -self.width / 2, (-self.height / 2) + (percent_ratio * self.height),
            self.width, 0.2 * self.height
        ))

    def draw_text_at_bounds(self, painter, option, widget, bounds: QRectF, text):
        font = QFont(painter.font())


        for size in range(self.maxFontHeight, self.minFontHeight - 1, -1):
            font.setPointSize(size)
            painter.setFont(font)

            metrics = QFontMetrics(font)
            bounding_rect = metrics.boundingRect(bounds.toRect(),
                                                 Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                                                 text)

            if bounding_rect.width() <= bounds.width() and bounding_rect.height() <= bounds.height():
                break

        # Final draw
        painter.setFont(font)
        painter.drawText(bounds, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)

    # Prints element type
    def paint_header(self, painter, option, widget, bounds: QRectF):
        if not self.header_text:
            return
        self.draw_text_at_bounds(painter, option, widget, bounds, self.header_text)

    # Prints descriptive graphic
    def paint_graphics(self, painter, option, widget, bounds: QRectF):
        self.draw_text_at_bounds(painter, option, widget, bounds, "No Graphics set")

        painter.drawLine(QLineF(
            bounds.x() + 0.1 * bounds.width(),
            bounds.y() + bounds.height() / 2,
            bounds.x() + bounds.width() - 0.1 * bounds.width(),
            bounds.y() + bounds.height() / 2
        ))

    # Prints element title
    def paint_title(self, painter, option, widget, bounds:QRectF):

        if not self.title_text:
            return
        self.draw_text_at_bounds(painter, option, widget, bounds, self.title_text)

    # Prints
    def paint_footer(self, painter, option, widget, bounds:QRectF):

        if not self.footer_text:
            return
        self.draw_text_at_bounds(painter, option, widget, bounds, self.footer_text)