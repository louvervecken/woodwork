import sys
import pathlib
import math

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from importlib import reload

import kinderkamer.closet as closet
import cadquery as cq
import woodwork.sheet as sheet
from cq_server.ui import ui, show_object

Sheet = sheet.BirchPly18
SheetBack = sheet.BirchPly6
SheetDoor = sheet.BirchPlyWhiteFinish18
SheetDraw = sheet.BirchPly12


DESK_HEIGHT = 750
DESK_WIDTH = 2000
DEPTH = 780
FEET = 110
CLOSET_WIDTH = 600
SLIDER_TH = 12.7
FRONT_SPACING = 5


class Desk(closet.SheetFurniture):
    def __init__(self) -> None:
        super().__init__('desk')
        blad = Sheet(DESK_WIDTH-CLOSET_WIDTH, DEPTH, plane='XY', name='blad', parent_name=self.name).set_z(DESK_HEIGHT - Sheet.THICK).set_x(CLOSET_WIDTH)
        onderblad = Sheet(DESK_WIDTH-CLOSET_WIDTH, 100, plane='XY', name='onderblad1', parent_name=self.name).set_z(DESK_HEIGHT - 2 * Sheet.THICK).set_x(CLOSET_WIDTH)
        onderblad2 = S
        heet(DESK_WIDTH-CLOSET_WIDTH, 100, plane='XY', name='onderblad2', parent_name=self.name)\
            .set_z(DESK_HEIGHT - 2 * Sheet.THICK).set_x(CLOSET_WIDTH).set_y(DEPTH - 100)

        self.sheets = [blad, onderblad, onderblad2]

class Shelves(closet.SheetFurniture):
    def __init__(self) -> None:
        super().__init__('shelves')
        shelve1_1 = Sheet(290, DEPTH, plane='XY', name='1_1', parent_name=self.name).set_z(DESK_HEIGHT + 600)
        shelve1_2 = Sheet(290, DEPTH, plane='XY', name='1_2', parent_name=self.name).set_z(DESK_HEIGHT + 600 + Sheet.THICK)
        shelve2_1 = Sheet(290, DEPTH, plane='XY', name='2_1', parent_name=self.name).set_z(DESK_HEIGHT + 600 * 2)
        shelve2_2 = Sheet(290, DEPTH, plane='XY', name='2_2', parent_name=self.name).set_z(DESK_HEIGHT + 600 * 2 + Sheet.THICK)

        self.sheets = [shelve1_1, shelve1_2, shelve2_1, shelve2_2]

        self.x = DESK_WIDTH - 290


class Closet(closet.SheetFurniture):
    def __init__(self):
        super().__init__(name='desk_kast')
        left = Sheet(DEPTH - SheetBack.THICK, DESK_HEIGHT - FEET, plane='YZ', name='left', parent_name=self.name)
        right = left.clone(name='right').set_x(CLOSET_WIDTH - Sheet.THICK)
        bottom = Sheet(CLOSET_WIDTH - 2 * Sheet.THICK, DEPTH - SheetBack.THICK, plane='XY', name='bottom', parent_name=self.name).set_x(Sheet.THICK)
        top = bottom.clone(name='top').set_x(Sheet.THICK).set_z(DESK_HEIGHT - FEET - Sheet.THICK)
        back = SheetBack(CLOSET_WIDTH, DESK_HEIGHT - FEET, plane='XZ', name='back', parent_name=self.name).set_y(DEPTH)

        self.sheets = [left, right, top, bottom, back]

        for dr_i in range(3):
            dr = DrawerWithFront(
                f"drawer_{dr_i}", 
                width=CLOSET_WIDTH - 2 * Sheet.THICK - 2 * SLIDER_TH, 
                depth=DEPTH - SheetDoor.THICK - SheetBack.THICK - 10, 
                height=(DESK_HEIGHT - FEET - Sheet.THICK*2 - 10) // 3 - 20 - SheetDraw.THICK,
                front_width=CLOSET_WIDTH - 2 * Sheet.THICK - 2 * FRONT_SPACING,
                front_height=((DESK_HEIGHT - FEET - Sheet.THICK*2) - (4 * FRONT_SPACING))//3,
                z_offset=5)
            dr.x = Sheet.THICK + FRONT_SPACING
            dr.z = Sheet.THICK + FRONT_SPACING + dr_i * (dr.front.height + 1 * FRONT_SPACING)
            self.sub_parts.append(dr)
        self.z = FEET


class Drawer(closet.SheetFurniture):
    def __init__(self, name, width, depth, height) -> None:
        super().__init__(name)
        left = SheetDraw(depth, height, plane='YZ', name='left', parent_name=self.name).set_z(SheetDraw.THICK)
        right = left.clone(name='right').set_x(width - SheetDraw.THICK).set_z(SheetDraw.THICK)
        back = SheetDraw(width - 2 * SheetDraw.THICK, height, plane='XZ', name='back', parent_name=self.name).set_x(SheetDraw.THICK)\
            .set_y(left.width).set_z(SheetDraw.THICK)
        front = back.clone(name='front').set_x(SheetDraw.THICK).set_z(SheetDraw.THICK).set_y(SheetDraw.THICK)
        bottom = SheetDraw(front.width + 2 * SheetDraw.THICK, left.width, plane='XY', name='bottom', parent_name=self.name)

        self.sheets = [left, right, back, front, bottom]


class DrawerWithFront(closet.SheetFurniture):
    def __init__(self, name, width, depth, height, front_width, front_height, z_offset) -> None:
        super().__init__(name)
        self.drawer = Drawer(f"drawer", width=width, depth=depth, height=height)
        self.drawer.x = (front_width - width) / 2
        self.drawer.y = SheetDoor.THICK
        self.drawer.z = z_offset

        self.front = SheetDoor(front_width, front_height, plane='XZ', name='front', parent_name=self.name).set_y(SheetDoor.THICK)

        self.sheets = (self.front, )
        self.sub_parts = (self.drawer, )
