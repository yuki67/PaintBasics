# -*- coding: utf-8 -*-
""" 図形を描くデモ """
import os
from math import cos, pi, sin
from tkinter import Tk, Canvas

from PIL import Image

from ColorArray.ExcelArrayPrinter import ExcelArrayPrinter
from ColorArray.HtmlArrayPrinter import HtmlArrayPrinter
from ColorArray.ShellArrayPrinter import ShellArrayPrinter
from Figure.Figure import Circle, Diamond, Ellipse, Line, Point, Polygon, ColorArray
from Painter.ColorArrayPainter import ColorArrayPainter
from Painter.JPGPainter import JPGPainter
from Painter.Painter import Painter
from Painter.TkPainter import TkPainter


def test_figure(painter: Painter,
                width: int,
                height: int) -> None:
    """ (width, height)のcanvasにpainterで図形描画 """
    p = [Point(1, 1, [0, 0, 0]),
         Point(width - 1, 1, [255, 255, 0]),
         Point(width - 1,
               height - 1, [255, 0, 255]),
         Point(1, height - 1, [0, 255, 255])]

    # Line, Polygon
    painter.draw(Polygon(p))
    painter.draw(Line(p[0], p[2]))
    painter.draw(Line(p[1], p[3]))

    # Ellipse,Circle
    center = Point(width / 2, height / 2, [0, 255, 0])
    painter.draw(Circle(center, width / 4))
    center.rgb = [0, 0, 255]
    painter.draw(Ellipse(center, width / 4, width / 2))
    center.rgb = [255, 0, 0]
    painter.draw(Ellipse(center, width / 2, width / 4))

    # Diamond
    painter.draw(Diamond(center,
                         width / 2,
                         16,
                         lambda t: [128 + 127 * sin(2 * pi * t),
                                    128 + 127 * cos(2 * pi * t),
                                    128 + 127 * sin(2 * pi * t) * cos(2 * pi * t)]))


def print_array(array: ColorArray, filename: str) -> None:
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
    foldername = "generated_files"
    if not os.path.exists(foldername):
        os.mkdir(foldername)

    # ArrayPainter
    width, height = 100, 100
    canvas = ColorArray(width, height)
    test_figure(ColorArrayPainter(canvas), width, height)
    print_array(canvas, os.path.join(foldername, "figure"))

    # JPGPainter
    width, height = 512, 512
    img = Image.new("RGB", (width, height), "white")
    test_figure(JPGPainter(img), width, height)
    img.save(os.path.join(foldername, "figure.jpg"))

    # TkPainter
    width, height = 512, 512
    root, canvas = setup_tk(512, 512)
    test_figure(TkPainter(canvas), width, height)
    canvas.place(x=5, y=5)
    root.mainloop()

    print("program ended.")

if __name__ == "__main__":
    prompt()
