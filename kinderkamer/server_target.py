from cq_server.ui import ui, show_object
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import woodwork.sheet as sheet
import cadquery as cq

from cadquery import exporters

from kinderkamer.desk import Desk
from kinderkamer.closet import fixed_closets
from kinderkamer.desk import Closet as DeskCloset
from kinderkamer.desk import Shelves


closets = fixed_closets()
desk = Desk()
desk_closet = DeskCloset()
shelves = Shelves()

ass = cq.Assembly(name='kinderkamer_two')
ass.add(desk.get_assembly())
ass.add(desk_closet.get_assembly(), loc=cq.Location(cq.Vector(desk_closet.x, desk_closet.y, desk_closet.z)))
ass.add(shelves.get_assembly(), loc=cq.Location(cq.Vector(shelves.x, shelves.y, shelves.z)))
ass.add(closets, loc=cq.Location(cq.Vector(0,0,0), cq.Vector((0, 0, 1)), 90) * cq.Location(cq.Vector(-3000, 1000,0)))
show_object(ass)

desk.export_step('./exports/bureau.step')
desk_closet.export_step('./exports/kast_bureau.step')
shelves.export_step('./exports/schappen.step')
exporters.export(closets.toCompound(), './exports/kasten.step')

sheet.BirchPly18.store_sheet_list()
sheet.BirchPly12.store_sheet_list()
sheet.BirchPly6.store_sheet_list()
sheet.BirchPlyWhiteFinish18.store_sheet_list()

pass