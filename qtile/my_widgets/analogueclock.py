# Copyright (c) 2022 elParaguayo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import math
from datetime import datetime

import cairocffi
from libqtile.log_utils import logger
from libqtile.widget import base

PI = math.pi


def to_rads(degrees):
    return degrees * PI / 180.0


class AnalogueClock(base._Widget):
    """
    An analogue clock for your Bar.
    """

    orientations = base.ORIENTATION_BOTH
    defaults = [
        ("foreground", None, "Shading for clock face"),
        ("hour_size", 2, "Thickness of hour hand"),
        ("hour_length", 0.5, "Length of hour hand as percentage of radius"),
        ("minute_size", 2, "Thickness of minute hand"),
        ("minute_length", 0.9,
         "Length of minute hand as percentage of radius"),
        ("second_size", 1, "Thickness of second hand, 0 to hide."),
        ("second_length", 1, "Length of minute hand as percentage of radius"),
        ("update_interval", 0.001, "Polling interval in secs."),
        ("margin", 0, "Margin around clock"),
        ("padding", 0, "Additional padding at edges of widget"),
        ("face_shape", None, "'square', 'circle' or None"),
        ("face_background", None, "Shading for clock face"),
        ("face_border_width", 2, "Thickness of clock face border"),
        ("face_border_colour", "00ffff", "Border colour for clock face"),
    ]

    _screenshots = [
        ("analogue_clock1.png", "Default config"),
        ("analogue_clock2.png", "With square clock face"),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, 0, **config)
        self.add_defaults(AnalogueClock.defaults)
        self.hours = self.minutes = self.minutes = 0
        self.clock_string = ""
        self.previous_clock = ""

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self.length = self.bar.size + 2 * self.padding
        self.drawer.ctx.set_antialias(cairocffi.ANTIALIAS_NONE)

        if self.face_shape not in ["square", "circle", None]:
            logger.warning("Unknown clock face shape. Setting to None.")
            self.face_shape = None

        if self.update_interval:
            self.timeout_add(self.update_interval, self.loop)

    def loop(self):
        self.timeout_add(self.update_interval, self.loop)
        self.update()

    def update(self):
        time = datetime.now()
        self.hours = time.hour % 12
        self.minutes = time.minute
        self.seconds = time.second
        self.clock_string = f"{self.hours}:{self.minutes}"
        self.draw(force=False)

    def _draw_hand(self, angle, thickness, length):
        self.drawer.ctx.save()
        self.drawer.ctx.translate(self.bar.size // 2 + self.padding,
                                  self.bar.size // 2 + thickness // 2)
        self.drawer.ctx.rotate(angle)
        self.drawer.set_source_rgb(self.foreground)
        self.drawer.ctx.set_line_width(thickness)
        self.drawer.ctx.move_to(0, 0)
        self.drawer.ctx.line_to((self.bar.size // 2 - self.margin) * length, 0)
        self.drawer.ctx.stroke()
        self.drawer.ctx.restore()

    def draw_face(self):
        if self.face_shape == "square":
            self.drawer.ctx.rectangle(
                self.padding + self.margin,
                self.margin,
                self.bar.size - 2 * self.margin,
                self.bar.size - 2 * self.margin,
            )
        else:
            self.drawer.ctx.arc(
                self.bar.size // 2 + self.padding,
                self.bar.size // 2,
                self.bar.size // 2 - self.margin,
                0,
                to_rads(360),
            )

        if self.face_background is not None:
            self.drawer.set_source_rgb(self.face_background)
            self.drawer.ctx.fill_preserve()

        if self.face_border_width:
            self.drawer.ctx.set_line_width(self.face_border_width)
            self.drawer.set_source_rgb(self.face_border_colour)
            self.drawer.ctx.stroke()

    def draw_hours(self):
        angle = ((self.hours / 12) + (self.minutes / (60 * 12))) * 360 - 90
        angle = to_rads(angle)
        self._draw_hand(angle, self.hour_size, self.hour_length)

    def draw_minutes(self):
        angle = (self.minutes / 60) * 360 - 90
        angle = to_rads(angle)
        self._draw_hand(angle, self.minute_size, self.minute_length)

    def draw_seconds(self):
        angle = (self.seconds / 60) * 360 - 90
        angle = to_rads(angle)
        self._draw_hand(angle, self.second_size, self.second_length)

    def draw(self, force=True):
        """
        Draws the clock.
        `force` parameter is True when called from self.bar.draw() so clock is always drawn.
        'force` is False when called on update. If the time is the same then we don't redraw
        the clock. Should save some CPU cycles on unnecessary drawing!
        """
        if not self.configured:
            return

        if not self.second_size and self.clock_string == self.previous_clock and not force:
            return

        self.drawer.clear(self.background or self.bar.background)

        if self.face_shape is not None and (self.face_background
                                            or self.face_border_width):
            self.draw_face()

        self.draw_hours()
        self.draw_minutes()
        if self.second_size:
            self.draw_seconds()

        self.drawer.draw(offsetx=self.offset,
                         offsety=self.offsety,
                         width=self.length)

        self.previous_clock = self.clock_string
