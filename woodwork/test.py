from cadquery import Workplane
from cq_server.ui import ui, show_object

model = Workplane("front").box(100, 200, 10)
show_object(model)
