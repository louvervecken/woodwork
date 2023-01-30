import pathlib
import cadquery as cq


class BirchPly18:
    COLOR = (218/255, 184/255, 136/255, 255)
    THICK = 18
    instances = list()
    
    def __init__(self, width, height, plane, name=None, parent_name=None):
        """
        plane: 'XY', 'XZ', 'YZ'
        """
        self.width = width
        self.height = height
        self.plane = plane
        self.name = name
        self.parent_name = parent_name
        self.box = cq.Workplane(plane).rect(width, height, centered=False).extrude(self.THICK)
        self.x = 0
        self.y = 0
        self.z = 0
        self.instances.append(self)

    def get_object(self):
        return self.box

    def set_x(self, x):
        self.x = x
        return self

    def set_y(self, y):
        self.y = y
        return self

    def set_z(self, z):
        self.z = z
        return self

    def clone(self, name=None):
        return type(self)(self.width, self.height, self.plane, name, self.parent_name)

    @classmethod
    def store_sheet_list(cls, file_name=None):
        if file_name is None:
            file_name = (pathlib.Path("./exports") / cls.__name__).with_suffix('.csv')
        print(file_name.resolve())
        file_name.parent.mkdir(exist_ok=True, parents=True)
        with open(file_name, 'w') as f:
            f.write("Length,Width,Qty,Label,Enabled\n")
            skip = list()
            for sheet in cls.instances:
                if sheet in skip:
                    continue
                count = 1
                for sh in cls.instances:
                    if sheet != sh and sheet.width == sh.width and sheet.height == sh.height:
                        count += 1
                        skip.append(sh)
                f.write(f"{sheet.height:.1f},{sheet.width:.1f}, {count},{sheet.label},True\n")

    @property
    def label(self):
        return f"{self.parent_name}_{self.name}_{self.plane}_w{int(self.width)}_h{int(self.height)}"



class BirchPly12(BirchPly18):
    THICK = 12
    instances = list()


class BirchPly9(BirchPly18):
    THICK = 9
    instances = list()


class BirchPly6(BirchPly18):
    THICK = 6
    instances = list()


class Mdf18(BirchPly18):
    COLOR = (.9, .9, .9, 255)
    instances = list()


class BirchPlyWhiteFinish18(BirchPly18):
    COLOR = (.9, .9, .9, 255)
    instances = list()
