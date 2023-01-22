import typing
import cadquery as cq

from woodwork import utils
import woodwork.sheet as sheet

from cq_server.ui import ui, show_object
from cadquery import exporters


FULL_WIDTH = 2500
DEPTH = 580
SPACING = 3
SHELVE_SPACING = 10
CEILING = 2450
FEET = 110

Sheet = sheet.BirchPly18
SheetBack = sheet.BirchPly6
SheetBackSide = sheet.BirchPly18
SheetDoor = sheet.BirchPlyWhiteFinish18
SheetShelve = sheet.BirchPly18


class SheetFurniture:
    def __init__(self, name) -> None:
        self.name = name
        self.sheets = list()
        self.sub_parts: typing.Sequence[SheetFurniture] = list()
        self.x = 0
        self.y = 0
        self.z = 0

    def get_assembly(self):
        ass = cq.Assembly(name=self.name)
        for sub_p in self.sub_parts:
            ass.add(sub_p.get_assembly(),
                    loc=cq.Location(cq.Vector(sub_p.x, sub_p.y, sub_p.z)),
                    name=sub_p.name)
        for sh in self.sheets:
            ass.add(
                sh.box, 
                loc=cq.Location(cq.Vector(sh.x, sh.y, sh.z)), 
                color=cq.Color(*sh.COLOR),
                name=sh.name)
        return ass
    
    def export_step(self, file_path):
        exporters.export(self.get_assembly().toCompound(), file_path)

    def show(self):
        show_object(self.get_assembly())


class ClosetUnit(SheetFurniture):
    def __init__(self, name, width, height):
        super().__init__(name)
        self.left = Sheet(DEPTH, height, plane='YZ', name='left')
        self.right = Sheet(DEPTH, height, plane='YZ', name='right').set_x(width - Sheet.THICK)
        self.bottom = Sheet(width - 2 * Sheet.THICK, DEPTH, plane='XY', name='bottom').set_x(Sheet.THICK)
        self.top = Sheet(width - 2 * Sheet.THICK, DEPTH, plane='XY', name='top')\
                   .set_x(Sheet.THICK).set_z(height - Sheet.THICK)
        self.back = SheetBack(width, height, plane='XZ', name='back').set_y(DEPTH + SheetBack.THICK)

        self.sheets = [self.left, self.right, self.bottom, self.top, self.back]


class ClosetDoorUnit(ClosetUnit):
    def __init__(self, name, width, height, shelves):
        super().__init__(name, width, height)
        self.door = SheetDoor(width - 2 * Sheet.THICK - 2 * SPACING, height - 2 * Sheet.THICK - 2 * SPACING,
                              plane='XZ', name='door').set_x(Sheet.THICK + SPACING).set_z(Sheet.THICK + SPACING).set_y(SheetDoor.THICK)
        self.sheets.append(self.door)

        self.shelve_list = list()
        for shelve in range(shelves):
            sh = SheetShelve(width - 2 * Sheet.THICK, DEPTH - SheetDoor.THICK - SHELVE_SPACING, plane='XY', name=f'shelve{shelve}')\
                .set_x(Sheet.THICK).set_y(SheetDoor.THICK + SHELVE_SPACING).set_z(height / (shelves + 1) * (shelve + 1))
            self.shelve_list.append(sh)
            self.sheets.append(sh)


class ClosetEdge(SheetFurniture):
    def __init__(self, name, width, height, open_edge='right'):
        super().__init__(name)
        self.side = Sheet(DEPTH - (SheetBackSide.THICK - SheetBack.THICK), height, plane='YZ', name=open_edge)
        self.bottom = Sheet(width - Sheet.THICK, DEPTH - (SheetBackSide.THICK - SheetBack.THICK), plane='XY', name='bottom')
        self.top = Sheet(width - Sheet.THICK, DEPTH - (SheetBackSide.THICK - SheetBack.THICK), plane='XY', name='top')

        if open_edge == 'left':
            self.side.set_x(width - Sheet.THICK)
        elif open_edge == 'right':
            self.bottom.set_x(Sheet.THICK)
            self.top.set_x(Sheet.THICK)

        self.top.set_z(height - Sheet.THICK)

        self.back = SheetBackSide(width, height, plane='XZ', name='back').set_y(DEPTH + SheetBack.THICK)

        self.sheets = [self.side, self.bottom, self.top, self.back]
        self.x = 0
        self.y = 0
        self.z = 0


def random_closets():
    widths = utils.randvec(FULL_WIDTH, 5, 800, 400)

    MID_SCALE_FACTOR = 0.4

    for wi, width in enumerate(widths):
        heights = utils.randvec(CEILING - FEET, 3, 1200, 400)
        heights[0] += heights[1] * (1 - MID_SCALE_FACTOR)
        # heights[2] += heights[1] * (1 - MID_SCALE_FACTOR)
        heights[1] *= MID_SCALE_FACTOR
        for hi, heigth in enumerate(heights):
            print(width, heigth)
            name = f'x{wi}_z{hi}'
            if hi in (0, 2):
                k = ClosetDoorUnit(name, width, heigth)
            else:
                if wi == 4:
                    k = ClosetEdge(name, width, heigth)
                else:
                    k = ClosetUnit(name, width, heigth)
            k.x = sum(widths[:wi])
            k.z = sum(heights[:hi]) + FEET


def fixed_closets():
    kasten = \
        (((460, 1057, 2), (460, 210, 0), (460, 1053, 2)),
         ((596, 1482, 0), (596, 360, 0), (596, 478, 1)),
         ((467, 1396, 3), (467, 300, 0), (467, 624, 1)),
         ((542, 1041, 2), (542, 456, 0), (542, 823, 2)),
         ((435, 1400, 3), (435, 370, 0), (435, 550, 1)))

    # kasten = \
    #     (((460, 1057, 0),),)

    col_pos = 0
    ass = cq.Assembly('kasten')
    for wi, col in enumerate(kasten):
        col_ass = cq.Assembly(f'colulm-{wi}')
        height_pos = 0
        for hi, (width, heigth, shelves) in enumerate(col):
            name = f'x{wi}_z{hi}'
            if hi in (0, 2):
                k = ClosetDoorUnit(name, width, heigth, shelves)
            else:
                if wi == 4:
                    k = ClosetEdge(name, width, heigth)
                elif wi == 0:
                    k = ClosetEdge(name, width, heigth, 'left')
                else:
                    k = ClosetUnit(name, width, heigth)
            k.x = col_pos
            k.z = height_pos + FEET
            height_pos += heigth
            col_ass.add(k.get_assembly(), name=f'row_{hi}', loc=cq.Location(cq.Vector(k.x, k.y, k.z)))
        ass.add(col_ass, name=f'column_{wi}')    
        col_pos += width
    return ass


# def feet():
#     front = Part.makeBox(FULL_WIDTH - 50, 60, FEET)
#     front.x = 25
#     front.y = 40
#     Part.show(front)
#     back = Part.makeBox(FULL_WIDTH - 50, 60, FEET)
#     back.x = 25
#     back.y = DEPTH - 60 - 50
#     Part.show(back)
