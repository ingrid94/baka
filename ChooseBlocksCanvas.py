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
    # x,y are upper left side corner coordinates, h is height of main block, w is width of main block
    # z is length of commands (when condition true) and lower block part to connect with other blocks
    def control_block_coords(x, y, h, w, z):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + w - 5, y, x + w, y + 5,
                  x + w, y + h - 5, x + w - 5, y + h,
                  x + 55, y + h, x + 50, y + h + 5,
                  x + 35, y + h + 5, x + 30, y + h,
                  x + 15, y + h, x + 10, y + h + 5,
                  x + 10, y + z + 35,
                  x, y + z + 35, x, y + 5]
        points_lower = [x + 10, y + z + 35, x + 15, y + z + 40,
                        x + 85, y + z + 40, x + 90, y + z + 45,
                        x + 90, y + z + 50,
                        x + 85, y + z + 55, x + 45, y + z + 55,
                        x + 40, y + z + 60, x + 25, y + z + 60,
                        x + 20, y + z + 55, x + 5, y + z + 55,
                        x, y + z + 50, x, y + z + 35]
        return [points, points_lower]

    @staticmethod
    def inside_block_coords(x, y, h, w):
        a = (h / 2)
        points = [x, y + a, x + a, y,
                  x + w, y, x + w + a, y + a,
                  x + w, y + h, x + a, y + h,
                  x, y + a]
        return points

    def create_blocks_fst(self):

        # block for print() command
        self.canvas.create_polygon(self.command_block_coords(50, 20, 30, 110), fill='violet red', outline='purple',
                                   tags='print_block')
        self.canvas.create_text(60, 30, anchor=NW, text='print(', tags='print_block')
        self.canvas.create_polygon(self.inside_block_coords(93, 30, 16, 40), fill='light pink', tags='print_block')
        self.canvas.create_text(147, 30, anchor=NW, text=')', tags='print_block')

        # block for return command
        self.canvas.create_polygon(self.command_block_coords(50, 60, 30, 110), fill='violet red', outline='purple',
                                   tags='return_block')
        self.canvas.create_text(60, 70, anchor=NW, text='return', tags='return_block')
        self.canvas.create_polygon(self.inside_block_coords(100, 70, 16, 40), fill='light pink', tags='return_block')

        # block for variable assignment command
        self.canvas.create_polygon(self.command_block_coords(50, 100, 30, 160), fill='violet red', outline='purple',
                                   tags='variable_block')
        self.canvas.create_polygon(self.inside_block_coords(60, 109, 16, 55), fill='dodger blue', outline='steel blue',
                                   tags='variable_block')
        self.canvas.create_text(70, 110, anchor=NW, text="variable", tags='variable_block')
        self.canvas.create_text(130, 105, anchor=NW, text="=", tags='variable_block', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(150, 110, 15, 40), fill='light pink', tags='variable_block')

        # block for list
        # self.canvas.create_polygon(self.command_block_coords(50, 140, 30, 180), fill='violet red', outline='purple',
        #                           tags='list_block')
        # self.canvas.create_polygon(self.inside_block_coords(60, 149, 16, 60), fill='dodger blue', outline='steel blue',
        #                           tags='list_block')
        # self.canvas.create_text(70, 150, anchor=NW, text="list name", tags='list_block')
        # self.canvas.create_text(135, 145, anchor=NW, text="= [", tags='list_block', font='bold')
        # self.canvas.create_text(210, 145, anchor=NW, text="]", tags='list_block', font='bold')
        # self.canvas.create_polygon(self.inside_block_coords(160, 150, 15, 40), fill='light pink', tags='list_block')

        # block for if statement
        self.canvas.create_polygon(self.control_block_coords(50, 180, 30, 110, 25)[0], fill='orange',
                                   outline='chocolate', tags='if_block')
        self.canvas.create_polygon(self.control_block_coords(50, 180, 30, 110, 25)[1], fill='orange',
                                   outline='chocolate', tags='if_block')
        self.canvas.create_text(70, 190, anchor=NW, text='if', tags='if_block')
        self.canvas.create_polygon(self.inside_block_coords(85, 189, 16, 55), fill='peachpuff', tags='if_block')

        # block for while statement
        self.canvas.create_polygon(self.control_block_coords(50, 270, 30, 115, 25)[0], fill='orange',
                                   outline='chocolate', tags='while_block')
        self.canvas.create_polygon(self.control_block_coords(50, 270, 30, 115, 25)[1], fill='orange',
                                   outline='chocolate', tags='while_block')
        self.canvas.create_text(60, 280, anchor=NW, text='while', tags='while_block')
        self.canvas.create_polygon(self.inside_block_coords(95, 279, 16, 55), fill='peachpuff', tags='while_block')

        # right side column
        # equals statement block
        self.canvas.create_polygon(self.inside_block_coords(300, 30, 20, 140), fill='dodger blue', outline='steel blue',
                                   tags='equals')
        self.canvas.create_polygon(self.inside_block_coords(310, 32, 16, 40), fill='sky blue', tags='equals')
        self.canvas.create_text(362, 29, anchor=NW, text="==", tags='equals', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 32, 16, 40), fill='sky blue', tags='equals')

        # not equal statement block
        self.canvas.create_polygon(self.inside_block_coords(300, 60, 20, 140), fill='dodger blue', outline='steel blue',
                                   tags='not_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 62, 16, 40), fill='sky blue', tags='not_equal')
        self.canvas.create_text(362, 60, anchor=NW, text="!=", tags='not_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 62, 16, 40), fill='sky blue', tags='not_equal')

        # grater than block
        self.canvas.create_polygon(self.inside_block_coords(300, 90, 20, 130), fill='dodger blue', outline='steel blue',
                                   tags='greater')
        self.canvas.create_polygon(self.inside_block_coords(310, 92, 16, 40), fill='sky blue', tags='greater')
        self.canvas.create_text(362, 90, anchor=NW, text=">", tags='greater', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(380, 92, 16, 40), fill='sky blue', tags='greater')

        # smaller than block
        self.canvas.create_polygon(self.inside_block_coords(300, 120, 20, 130), fill='dodger blue', outline='steel blue',
                                   tags='smaller')
        self.canvas.create_polygon(self.inside_block_coords(310, 122, 16, 40), fill='sky blue', tags='smaller')
        self.canvas.create_text(362, 120, anchor=NW, text="<", tags='smaller', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(380, 122, 16, 40), fill='sky blue', tags='smaller')

        # grater or equal block
        self.canvas.create_polygon(self.inside_block_coords(300, 150, 20, 140), fill='dodger blue', outline='steel blue',
                                   tags='greater_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 152, 16, 40), fill='sky blue', tags='greater_or_equal')
        self.canvas.create_text(362, 150, anchor=NW, text=">=", tags='greater_or_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 152, 16, 40), fill='sky blue', tags='greater_or_equal')

        # smaller or equal block
        self.canvas.create_polygon(self.inside_block_coords(300, 180, 20, 140), fill='dodger blue', outline='steel blue',
                                   tags='smaller_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, 182, 16, 40), fill='sky blue', tags='smaller_or_equal')
        self.canvas.create_text(362, 180, anchor=NW, text="<=", tags='smaller_or_equal', font='bold')
        self.canvas.create_polygon(self.inside_block_coords(390, 182, 16, 40), fill='sky blue', tags='smaller_or_equal')

        # or block
        self.canvas.create_polygon(self.inside_block_coords(300, 210, 20, 130), fill='dodger blue',
                                   outline='steel blue', tags='or')
        self.canvas.create_polygon(self.inside_block_coords(310, 212, 16, 40), fill='sky blue', tags='or')
        self.canvas.create_text(365, 212, anchor=NW, text="or", tags='or')
        self.canvas.create_polygon(self.inside_block_coords(385, 212, 16, 40), fill='sky blue', tags='or')

        # and block
        self.canvas.create_polygon(self.inside_block_coords(300, 240, 20, 130), fill='dodger blue',
                                   outline='steel blue', tags='and')
        self.canvas.create_polygon(self.inside_block_coords(310, 242, 16, 40), fill='sky blue', tags='and')
        self.canvas.create_text(362, 242, anchor=NW, text="and", tags='and')
        self.canvas.create_polygon(self.inside_block_coords(385, 242, 16, 40), fill='sky blue', tags='and')

        # not block
        self.canvas.create_polygon(self.inside_block_coords(300, 270, 20, 90), fill='dodger blue',
                                   outline='steel blue', tags='not')
        self.canvas.create_text(315, 272, anchor=NW, text='not', tags='not')
        self.canvas.create_polygon(self.inside_block_coords(340, 272, 16, 40), fill='sky blue', tags='not')

        # block for variable
        self.canvas.create_polygon(self.inside_block_coords(300, 300, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='variable')
        self.canvas.create_text(312, 300, anchor=NW, text="variable", tags='variable')

        # block for creating number
        self.canvas.create_polygon(self.inside_block_coords(300, 330, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='number')
        self.canvas.create_text(312, 330, anchor=NW, text="number", tags='number')

        # block for creating string
        self.canvas.create_polygon(self.inside_block_coords(300, 360, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='string')
        self.canvas.create_text(315, 360, anchor=NW, text="string", tags='string')

        # None block
        self.canvas.create_polygon(self.inside_block_coords(400, 300, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='none')
        self.canvas.create_text(415, 300, anchor=NW, text="None", tags='none')

        # True block
        self.canvas.create_polygon(self.inside_block_coords(400, 330, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='true')
        self.canvas.create_text(415, 330, anchor=NW, text="True", tags='true')

        # False block
        self.canvas.create_polygon(self.inside_block_coords(400, 360, 15, 63), fill='dodger blue', outline='steel blue',
                                   tags='false')
        self.canvas.create_text(415, 360, anchor=NW, text="False", tags='false')

    def bind(self, function):
        self.canvas.bind("<ButtonPress-1>", function)
