# -*- coding: utf-8 -*-
import os
from math import cos, pi, sin
from tkinter import Tk, Canvas
from typing import Union

from ColorArray.ExcelArrayPrinter import ExcelArrayPrinter
from ColorArray.HtmlArrayPrinter import HtmlArrayPrinter
from ColorArray.ShellArrayPrinter import ShellArrayPrinter
from Painter.ColorArrayPainter import ColorArrayPainter
from Painter.Figure import Circle, Diamond, Ellipse, Line, Point, Polygon, ColorArray
from Painter.Painter import Painter
from Painter.TkPainter import TkPainter


def test_figure(canvas: Union[Canvas, ColorArray],
                painter: Painter,
                width: int,
                height: int) -> None:
    """ 図形描画のテスト """
    p = [Point(1, 1, [0, 0, 0]),
         Point(width - 1, 1, [255, 255, 0]),
         Point(width - 1,
               height - 1, [255, 0, 255]),
         Point(1, height - 1, [0, 255, 255])]

    # Line, Polygon
    painter.draw(canvas, Polygon(p))
    painter.draw(canvas, Line(p[0], p[2]))
    painter.draw(canvas, Line(p[1], p[3]))

    # Ellipse,Circle
    center = Point(width / 2, height / 2, [0, 255, 0])
    painter.draw(canvas, Circle(center, width / 4))
    center.rgb = [0, 0, 255]
    painter.draw(canvas, Ellipse(center, width / 4, width / 2))
    center.rgb = [255, 0, 0]
    painter.draw(canvas, Ellipse(center, width / 2, width / 4))

    # Diamond
    painter.draw(canvas,
                 Diamond(center,
                         width / 2,
                         16,
                         lambda t: [128 + 127 * sin(2 * pi * t),
                                    128 + 127 * cos(2 * pi * t),
                                    128 + 127 * sin(2 * pi * t) * cos(2 * pi * t)]))


def draw_array_printer(array: ColorArray, filename: str) -> None:
    """ arrayPainterを使ってarrayを描く """
    ExcelArrayPrinter(filename).print(array)
    ShellArrayPrinter(filename).print(array)
    HtmlArrayPrinter(filename).print(array)


def setup_tk(width: int, height: int) -> (Tk, Canvas):
    """ Tkのrootとcanvasを作って返す """
    root = Tk()
    root.title("Tk Painter")
    root.geometry("%dx%d+%d+%d" % (width + 10, height + 10, 256, 0))
    canvas = Canvas(root, width=width, height=height)
    return root, canvas


def prompt() -> None:
    """ 対話処理など """

    # ArrayPainter
    width, height = 100, 100
    canvas = ColorArray(width, height)
    test_figure(canvas, ColorArrayPainter(), width, height)

    if not os.path.exists("figures"):
        os.mkdir("figures")
    draw_array_printer(canvas, os.path.join("figures", "figure"))

    # TkPainter
    width, height = 512, 512
    root, canvas = setup_tk(512, 512)
    test_figure(canvas, TkPainter(), width, height)
    canvas.place(x=5, y=5)
    root.mainloop()
    print("program ended.")


prompt()
