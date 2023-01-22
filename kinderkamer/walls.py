import FreeCAD
import Part

THICK = 100
HEIGHT = 2500


def draw():
    w1 = Part.makeBox(2370, 1, HEIGHT)
    Part.show(w1)
    w2 = Part.makeBox(1, 780, HEIGHT)
    Part.show(w2)
    w3 = Part.makeBox(290, 1, HEIGHT)
    w3.Placement.Base.y = 780
    Part.show(w3)
    w4 = Part.makeBox(1, 935, HEIGHT)
    w4.Placement.Base.y = 780
    w4.Placement.Base.x = 290
    Part.show(w4)
    w5 = Part.makeBox(290, 1, HEIGHT)
    w5.Placement.Base.y = 780 + 935
    Part.show(w5)


if __name__ == '__main__':
    #FreeCAD.newDocument()
    draw()
    FreeCAD.ActiveDocument.recompute()
    # FreeCAD.ActiveDocument.ActiveView.setCameraOrientation((1, 0, 0, 1))
