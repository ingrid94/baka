from tkinter import *


class ChooseBlocksCanvas:
    def __init__(self, root):
        self.top = Toplevel(root)
        self.canvas = Canvas(self.top, width=500, height=500, bg="white", highlightthickness=0)
        self.canvas.pack()

    def get_focus_set(self):
        return self.canvas.focus_set()

    def gettags(self, int):
        return self.canvas.gettags(int)

    @staticmethod
    def command_block_coords(x, y, h, w):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + w - 5, y, x + w, y + 5,
                  x + w, y + h - 5, x + w - 5, y + h,
                  x + 45, y + h, x + 40, y + h + 5,
                  x + 25, y + h + 5, x + 20, y + h,
                  x + 5, y + h, x, y + h - 5,
                  x, y + 5]
        return points

    @staticmethod
    # x,y are upper left side corner coordinates, z is height of main block,
    # w is length of commands (when condition true) and lower block part to connect with other blocks
    def control_block_coords(x, y, z, w):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + 175, y, x + 180, y + 5,
                  x + 180, y + z - 5, x + 175, y + z,
                  x + 55, y + z, x + 50, y + z + 5,
                  x + 35, y + z + 5, x + 30, y + z,
                  x + 15, y + z, x + 10, y + z + 5,
                  x + 10, y + w + 35,
                  x, y + w + 35, x, y + 5]
        points_lower = [x + 10, y + w + 35, x + 15, y + w + 40,
                        x + 85, y + w + 40, x + 90, y + w + 45,
                        x + 90, y + w + 50,
                        x + 85, y + w + 55, x + 45, y + w + 55,
                        x + 40, y + w + 60, x + 25, y + w + 60,
                        x + 20, y + w + 55, x + 5, y + w + 55,
                        x, y + w + 50, x, y + w + 35]
        return [points, points_lower]

    @staticmethod
    def inside_block_coords(x, y, w, h):
        a = (h / 2)
        points = [x, y + a, x + a, y,
                  x + w, y, x + w + a, y + a,
                  x + w, y + h, x + a, y + h,
                  x, y + a]
        return points

    @staticmethod
    def type_block_coords(x, y, w, h):
        points = [x, y,
                  x + w, y,
                  x + w, y + h,
                  x, y + h,
                  x, y]
        return points

    def create_blocks_fst(self):
        # block for print() command
        self.canvas.create_polygon(self.command_block_coords(50, 20, 30, 110), fill='violet red', outline='purple',
                                   tags='print_block')
        self.canvas.create_text(60, 30, anchor=NW, text='print(', tags='print_block')
        self.canvas.create_polygon(self.inside_block_coords(93, 30, 40, 16), fill='light pink', tags='print_block')
        self.canvas.create_text(147, 30, anchor=NW, text=')', tags='print_block')

        # block for return command
        self.canvas.create_polygon(self.command_block_coords(50, 60, 30, 110), fill='violet red', outline='purple',
                                   tags='return_block')
        self.canvas.create_text(60, 70, anchor=NW, text='return', tags='return_block')
        self.canvas.create_polygon(self.inside_block_coords(100, 70, 40, 16), fill='light pink', tags='return_block')

        # block for variable assignment command
        self.canvas.create_polygon(self.command_block_coords(50, 100, 30, 160), fill='violet red', outline='purple',
                                   tags='variable_block')
        self.canvas.create_polygon(self.inside_block_coords(60, 109, 55, 16), fill='limegreen', outline='green',
                                   tags='variable_block')
        self.canvas.create_text(70, 110, anchor=NW, text="variable", tags='variable_block')
        self.canvas.create_text(130, 105, anchor=NW, text="=", tags='variable_block', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(150, 110, 40, 15), fill='light pink', tags='variable_block')

        # self.canvas.create_polygon(self.inside_block_coords(50, 110, 130, 20), fill='dodger blue',
        # outline='steel blue', tags='inside_block')
        # self.canvas.create_polygon(self.inside_block_coords(50, 250, 65, 20), fill='limegreen', outline='green')

        self.canvas.create_polygon(self.control_block_coords(50, 150, 30, 35)[0], fill='orange', outline='chocolate',
                                   tags='control_block')
        self.canvas.create_polygon(self.control_block_coords(50, 150, 30, 35)[1], fill='orange', outline='chocolate',
                                   tags='control_block')

        self.canvas.create_polygon(self.inside_block_coords(50, 260, 63, 15), fill='limegreen', outline='green',
                                   tags='variable')
        self.canvas.create_text(62, 260, anchor=NW, text="variable", tags='variable')

        self.canvas.create_polygon(self.inside_block_coords(50, 290, 63, 15), fill='limegreen', outline='green',
                                   tags='number')
        self.canvas.create_text(62, 290, anchor=NW, text="number", tags='number')

        self.canvas.create_polygon(self.inside_block_coords(50, 320, 63, 15), fill='limegreen', outline='green',
                                   tags='string')
        self.canvas.create_text(65, 320, anchor=NW, text="string", tags='string')

        self.canvas.create_polygon(self.inside_block_coords(50, 350, 63, 15), fill='limegreen', outline='green',
                                   tags='none')
        self.canvas.create_text(65, 350, anchor=NW, text="None", tags='none')

        self.canvas.create_polygon(self.inside_block_coords(50, 380, 63, 15), fill='dodger blue', outline='steel blue',
                                   tags='true')
        self.canvas.create_text(65, 380, anchor=NW, text="True", tags='true')

        self.canvas.create_polygon(self.inside_block_coords(50, 410, 63, 15), fill='dodger blue', outline='steel blue',
                                   tags='false')
        self.canvas.create_text(65, 410, anchor=NW, text="False", tags='false')

        # right side column
        self.canvas.create_polygon(self.inside_block_coords(300, 30, 140, 20), fill='dodger blue', outline='steel blue',
                                   tags='equals')
        self.canvas.create_polygon(self.inside_block_coords(310, 32, 40, 16), fill='sky blue', tags='equals')
        self.canvas.create_text(362, 29, anchor=NW, text="==", tags='equals', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 32, 40, 16), fill='sky blue', tags='equals')

        self.canvas.create_polygon(self.inside_block_coords(300, 60, 140, 20), fill='dodger blue', outline='steel blue',
                                   tags='not_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 62, 40, 16), fill='sky blue', tags='not_equal')
        self.canvas.create_text(362, 60, anchor=NW, text="!=", tags='not_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 62, 40, 16), fill='sky blue', tags='not_equal')

        self.canvas.create_polygon(self.inside_block_coords(300, 90, 130, 20), fill='dodger blue', outline='steel blue',
                                   tags='greater')
        self.canvas.create_polygon(self.inside_block_coords(310, 92, 40, 16), fill='sky blue', tags='greater')
        self.canvas.create_text(362, 90, anchor=NW, text=">", tags='greater', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(380, 92, 40, 16), fill='sky blue', tags='greater')

        self.canvas.create_polygon(self.inside_block_coords(300, 120, 130, 20), fill='dodger blue', outline='steel blue',
                                   tags='smaller')
        self.canvas.create_polygon(self.inside_block_coords(310, 122, 40, 16), fill='sky blue', tags='smaller')
        self.canvas.create_text(362, 120, anchor=NW, text="<", tags='smaller', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(380, 122, 40, 16), fill='sky blue', tags='smaller')

        self.canvas.create_polygon(self.inside_block_coords(300, 150, 140, 20), fill='dodger blue', outline='steel blue',
                                   tags='greater_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 152, 40, 16), fill='sky blue', tags='greater_or_equal')
        self.canvas.create_text(362, 150, anchor=NW, text=">=", tags='greater_or_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 152, 40, 16), fill='sky blue', tags='greater_or_equal')

        self.canvas.create_polygon(self.inside_block_coords(300, 180, 140, 20), fill='dodger blue', outline='steel blue',
                                   tags='smaller_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 182, 40, 16), fill='sky blue', tags='smaller_or_equal')
        self.canvas.create_text(362, 180, anchor=NW, text="<=", tags='smaller_or_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 182, 40, 16), fill='sky blue', tags='smaller_or_equal')

        self.canvas.create_polygon(self.inside_block_coords(300, 210, 130, 20), fill='dodger blue',
                                   outline='steel blue', tags='or')
        self.canvas.create_polygon(self.inside_block_coords(310, 212, 40, 16), fill='sky blue', tags='or')
        self.canvas.create_text(365, 212, anchor=NW, text="or", tags='or')
        self.canvas.create_polygon(self.inside_block_coords(385, 212, 40, 16), fill='sky blue', tags='or')

        self.canvas.create_polygon(self.inside_block_coords(300, 240, 130, 20), fill='dodger blue',
                                   outline='steel blue', tags='and')
        self.canvas.create_polygon(self.inside_block_coords(310, 242, 40, 16), fill='sky blue', tags='and')
        self.canvas.create_text(362, 242, anchor=NW, text="and", tags='and')
        self.canvas.create_polygon(self.inside_block_coords(385, 242, 40, 16), fill='sky blue', tags='and')

        self.canvas.create_polygon(self.inside_block_coords(300, 270, 90, 20), fill='dodger blue',
                                   outline='steel blue', tags='not')
        self.canvas.create_text(315, 272, anchor=NW, text='not', tags='not')
        self.canvas.create_polygon(self.inside_block_coords(340, 272, 40, 16), fill='sky blue', tags='not')

    def bind(self, function):
        self.canvas.bind("<ButtonPress-1>", function)
